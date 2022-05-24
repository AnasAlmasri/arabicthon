function showOrHideSearchFields(action, fieldList) {
    for (let i = 0; i < fieldList.length; i++) {
        if (action == 'show') $('#' + fieldList[i]).show();
        if (action == 'hide') $('#' + fieldList[i]).hide();
    }
}
function renderSearchForm(mode) {
    $("#poet_details_div").hide();
    $("#get_poems_div").hide();
    switch (mode) {
        case 'poet':
            $("#radio_poet").prop("checked", true);
            $("#radio_bayt").prop("checked", false);
            showOrHideSearchFields('show', ['poet_name_div']);
            showOrHideSearchFields('hide', ['keyword_div', 'bahr_div', 'age_div']);
            break;
        case 'bayt':
            $("#radio_poet").prop("checked", false);
            $("#radio_bayt").prop("checked", true);
            showOrHideSearchFields('show', ['keyword_div', 'bahr_div', 'age_div']);
            showOrHideSearchFields('hide', ['poet_name_div']);
            break;
        default:
            renderSearchForm('bayt');
    }
}

function getPoetDetails(poet_name) {
    $.ajax({
        type: "POST",
        url: "/poet_details/",
        data: { "poet_name": poet_name },
        success: function (response) {
            // hide search form
            $("#search_form").hide();
            $("#get_poems_div").hide();

            // set text
            $("#poet_paragraph").text(response["text"]);
            $("#hidden_poet_name").val(poet_name);

            // show poet details
            $("#poet_details_div").show();
        }
    });
}

function getPoems() {
    poet_name = $("#hidden_poet_name").val();
    $.ajax({
        type: "POST",
        url: "/get_poems/",
        data: { "poet_name": poet_name },
        success: function (response) {
            // hide search form
            $("#search_form").hide();

            // hide poet details
            $("#poet_details_div").hide();

            // set header text
            $("#reader_poet_name").text("مما كتبه " + poet_name);

            // build table content
            var table_content = "";
            for (var i = 0; i < response["content"].length; i++) {
                var obj = response["content"][i];
                table_content += "<tr>" + "<td>" + obj.shatr_left + "</td>" + "<td>" + obj.shatr_right + "</td>" + "</tr>"
            }

            $("#poems_of_poet > tbody").html(table_content);

            // show poems
            $("#get_poems_div").show();
        }
    });
}

function renderPoems(poems) {
    // clean up and parse json
    var re = new RegExp('&quot;', 'g');
    poems = JSON.parse(poems.replace(re, '"'));

    // hide search form
    $("#search_form").hide();

    // hide poet details
    $("#poet_details_div").hide();

    // set header text
    $("#reader_poet_name").text("");

    // build table content
    var table_content = "";
    for (var i = 0; i < poems.length; i++) {
        var obj = poems[i];
        table_content += "<tr>" + "<td>" + obj.shatr_left + "</td>" + "<td>" + obj.shatr_right + "</td>" + "</tr>"
    }

    $("#poems_of_poet > tbody").html(table_content);

    // show poems
    $("#get_poems_div").show();
}
