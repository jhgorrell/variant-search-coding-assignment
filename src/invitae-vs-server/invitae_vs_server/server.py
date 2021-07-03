#
# invitae-hw-variant-search/src/invitae-vs-server/invitae_vs_server/server.py ---
#

import os
import pprint
import traceback

import flask
import flask_bootstrap
from invitae_vs_core.util import (
    safe_int,
)
from invitae_vs_core.vs_core import (
    VS_Core,
)

#####

#: Vars we get from the env and pass to the templates.
TMPL_ENV_VAR_NAMES = [
    "INVITAE_VS_CLIENT",
    "INVITAE_VS_DATA_DIR",
    "INVITAE_VS_DATA_TSV",
    "INVITAE_VS_DB_URI",
    "INVITAE_VS_DEBUG",
    "INVITAE_VS_DEPLOY",
    "INVITAE_VS_DIR",
    "INVITAE_VS_SERVER_PORT",
    "INVITAE_VS_SQLITE_FILE",
    "INVITAE_VS_VE_DIR",
]

#:
TMPL_VARS = dict()


def tmpl_vars_generate():
    #
    for name in TMPL_ENV_VAR_NAMES:
        val = os.environ.get(name)
        # also put into the global env.
        globals()[name] = val
        #
        TMPL_VARS[name] = val
    #
    env_vars = dict(TMPL_VARS)
    TMPL_VARS["ENV_VARS"] = env_vars


tmpl_vars_generate()

#####

app = flask.Flask(
    __name__,
    static_folder="./static")

# app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
bootstrap = flask_bootstrap.Bootstrap(app)

#####


@app.context_processor
def inject_env_vars():
    """Add our template vars to the global template context.
    """
    return TMPL_VARS

#####

# nginx redirect is broken?
# @app.route("/")
# def main():
#     """Redirect "/" to the search page."""
#     return flask.redirect(flask.url_for('search'))


@app.route("/server_info")
def server_info():
    """Show info about this server.
    Handy for debugging.
    """
    return flask.render_template("server_info_page.html")

#####

@app.route("/")
@app.route("/search")
def search():
    """The page to search our variants.
    """
    # TODO: pass along the search args like "?gene=NAME"
    #       so the result box can be filled in.

    # TODO: there is still a warning in the Chrome console about this.
    #       need to read more.
    resp = flask.make_response(
        flask.render_template("search_page.html"))
    resp.set_cookie("PHPSESSID", samesite="Strict")
    return resp


@app.route(
    "/gene_search_api_v1",
    methods=["GET", "POST"])
def gene_search_api_v1():
    """Search and return the data.
    """

    # pprint.pprint(flask.request)

    try:
        args = flask.request.get_json(force=True)
    except BaseException:
        traceback.print_exc()
        args = dict()

    # pprint.pprint(args)

    vs_core = VS_Core()
    rows = vs_core.query_variant(
        q_limit=safe_int(args.get("f_limit")),
        q_gene_name=args.get("f_gene_name"),
        q_genomic_start_range=args.get("f_genomic_start"),
        q_genomic_stop_range=args.get("f_genomic_stop"))

    table_rows = []
    for row in rows:
        table_row = dict()
        table_rows.append(table_row)

        # Add more if wanted.
        for name in [
                "gene", "chr",
                "genomic_start", "genomic_stop",
                "ref", "alt", "accession", ]:
            table_row[name] = getattr(row, name)

    data = {
        "rows": table_rows,
    }
    #
    return flask.jsonify(data)

@app.route(
    "/gene_autocomplete_api_v1",
    methods=["GET", "POST"])
def gene_autocomplete_api_v1():
    """Generate gene auto-completions for the next char.
    """

    try:
        args = flask.request.get_json(force=True)
    except:
        args={}

    prefix=args.get("prefix","")

    vs_core = VS_Core()
    rows = vs_core.gene_autocomplete(prefix=prefix)

    data={
        "autocomplete": rows,
    }
    return flask.jsonify(data)
