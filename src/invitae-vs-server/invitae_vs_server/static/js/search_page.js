//
// invitae-vs-server/invitae_vs_server/static/js/search_page.js ---
//
// Loaded with the search page.

console.log("loaded 'search_page.js'");

// Send the query to the server and update the search results.
function vs_do_search() {
  console.log("vs_do_search");

  var data={
      f_gene_name: $("#f_gene_name").val(),
      f_genomic_start: $("#f_genomic_start").val(),
      f_genomic_stop: $("#f_genomic_stop").val(),
      f_limit: $("#f_limit").val()
  };

  // console.log(data);

  $.ajax({
    method: "POST",
    url: "/gene_search_api_v1",
    data: JSON.stringify(data),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
  })
  .done(function (result) {
    // console.log(msg);
    //
    var tbl=$("#vs_results_table").DataTable();
    tbl.clear();

    result.rows.forEach(function (value,idx,array) {
      // console.log(value);
      tbl.row.add([
        value.gene,
        value.chr,
        value.genomic_start,
        value.genomic_stop,
        value.ref,
        value.alt,
        value.accession
        ]).draw(false);
    });

    tbl.draw();
  });
}

function vs_gene_name_autocomplete(ac_request, ac_response_func) {
  $.ajax({
    method: "POST",
    url: "/gene_autocomplete_api_v1",
    data: JSON.stringify({
      prefix: ac_request.term
    }),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
  })
      .done(function (rpc_result) {
        // console.log(rpc_result);
        ac_response_func(rpc_result.autocomplete);
      });
}

/////

$(document).ready(function() {

  $('#vs_results_table').DataTable({
    "paging": false,
    "order": [[1]]
  });

  $('#f_gene_name').autocomplete({
    source: vs_gene_name_autocomplete});

});
