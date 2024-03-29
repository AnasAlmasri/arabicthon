function showOrHideSearchFields(action, fieldList) {
    for (let i = 0; i < fieldList.length; i++) {
        if (action == 'show') $('#' + fieldList[i]).show();
        if (action == 'hide') $('#' + fieldList[i]).hide();
    }
}
function renderSearchForm(mode) {
    $("#poet_details_div").hide();
    $("#get_poems_div").hide();
    $("#poem_options").hide();
    $("#poet_details_div").hide();
    switch (mode) {
        case 'poet':
            $("#radio_poet").prop("checked", true);
            $("#radio_bayt").prop("checked", false);
            showOrHideSearchFields('show', ['poet_name_div', 'poet_dd_div']);
            showOrHideSearchFields('hide', ['keyword_div', 'bahr_div', 'age_div']);
            break;
        case 'bayt':
            $("#radio_poet").prop("checked", false);
            $("#radio_bayt").prop("checked", true);
            showOrHideSearchFields('show', ['keyword_div', 'bahr_div', 'age_div']);
            showOrHideSearchFields('hide', ['poet_name_div', 'poet_dd_div']);
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
            $("#poet_container").hide();

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
            $("#back_btn").show();

            $("#poem_options").show();

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
        table_content += "<tr>" + "<td class=\"clickableRow\">" + obj.shatr_left + "</td>" + "<td class=\"clickableRow\">" + obj.shatr_right + "</td>" + "</tr>"
    }

    $("#poems_of_poet > tbody").html(table_content);

    // show poems
    $("#get_poems_div").show();
    $("#back_btn").show();
}

function renderOptions() {
    $("#poem_options").show();
    $("#poet_details_div").hide();
}

function getMeaning() {
    var word = $("#word_search").val();
    $.ajax({
        type: "POST",
        url: "/get_meaning/",
        data: { "word": word },
        success: function (response) {
            $("#word_meaning").html('<div class="alert info"><span style="float: right; font-size: 16px; direction: rtl; font-family: AlmaraiRegular !important;">' + response["meaning"] + '</span></div>');
        }
    });
}

function getSentiment() {
    var text = "";
    $(".highlight").each(function () {
        $.each(this.cells, function () {
            text += $(this).text() + " ";
        });
    });

    $.ajax({
        type: "POST",
        url: "/get_sentiment/",
        data: { "text": text },
        success: function (response) {
            $("#sentiment").html('<div class="alert info"><span style="float: center; font-size: 16px; direction: rtl; font-family: AlmaraiRegular !important;">' + response["pred"] + '</span></div>');
        }
    });
}

function getPrediction() {
    var poet = "";
    var text = $("#model_word_search").val();

    if ($("#model_poet").length) {
        poet = $("#model_poet").val();
    } else {
        poet = $("#hidden_poet_name").val();

    }
    $("#loader_div").show();

    $.ajax({
        type: "POST",
        url: "/get_prediction/",
        tryCount: 0,
        retryLimit: 3,
        data: { "poet": poet, "text": text },
        success: function (response) {
            $("#poem_generator").html('<div class="alert info"><span style="float: right; font-size: 16px; direction: rtl; font-family: AlmaraiRegular !important;">' + response["pred"] + '</span></div>');
            $("#loader_div").hide();
        },
        error: function (xhr, textStatus, errorThrown) {
            if (textStatus == 'timeout') {
                this.tryCount++;
                if (this.tryCount <= this.retryLimit) {
                    //try again
                    setTimeout($.ajax(this), 3000);
                    return;
                }
                return;
            }
            if (xhr.status == 500) {
                //handle error
            } else {
                $("#loader_div").show();
            }
        }
    });
}
