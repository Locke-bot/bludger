var options = $("#id_url_visit_count option") 
var related = $("div.related-widget-wrapper a")
var relatedLinks = $("<div />") // just a container, won't feature
related_string = ''
for (let i=0; related.length > i; i++){
    $(related[i]).appendTo(relatedLinks)
    if (i == 0){ //change
        $(related[i]).attr("href", "/harry-potter-and-the-half-blood-prince/facet_one/urlcount/substitute/change/?_to_field=id&_popup=1")
    }
    else if (i == 2){ //delete
        $(related[i]).attr("href", "/harry-potter-and-the-half-blood-prince/facet_one/urlcount/substitute/delete/?_to_field=id&_popup=1")
    }
}
relatedLinks = relatedLinks.html()
select = $("#id_url_visit_count")
table = $('<table />', {
        id: "id_url_visit_count"
    })
for (let i=1; i < options.length; i++){
    option  = $(options[i])
    values = option.html().split(" ")
    date = values.shift() + " " + values.shift() + " " + values.shift()
    noOfTimes = values.pop()
    if ((values.reduce((a, x) => a += " " + x)) == $("#id_descriptor").val()){
        tr = $("<tr />", {
            })
        $("<td />", {
            text: date
        }).appendTo(tr)
        $("<td />", {
            text: noOfTimes
            }).appendTo(tr) 
        $("<td>" + relatedLinks.replaceAll("substitute", option.attr("value")) + "</td>").appendTo("<td />").appendTo(tr)        
        tr.appendTo(table)
    }
} 
table.insertAfter("#id_url_visit_count")
select.remove() 