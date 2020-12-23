var image = 3;
var text = 1;
function spawner(mode){
    cd = document.getElementsByTagName('fieldset')[0]
    author = document.getElementById('id_author')
    body = document.getElementById('id_body') 
    title = document.getElementById('id_title')
    if (mode==1){
        for (let i=1; i < text; i++){
            console.log(i)
            document.getElementById("id_text_"+i).innerHTML = document.getElementById("id_text_"+i).value
        } 
        value = title.value
        type = author.value
        body.innerHTML = body.value
        image_id = "id_image_"+image
        file_input = '<div class="form-row field-image" id="' + "div_image_"+image + '">\
        <label for="' + image_id + '">Image:</label>\
        <input type="file" name="image" accept="image/*" id="' + image_id + '" onclick=romero(' + image + ');>\
        <select name="image_class" required="" id="id_author">\
        <option value="1" selected>Block</option>\
        <option value="2">Inline</option>\
        </select>\
        &nbsp;&nbsp;<span id="' + "span_image_"+image + '"></span>&nbsp;&nbsp;\
        <input type="button" value="remove" onclick=remover(1,' + image_id + ');><br>\
        <label for="' + "span_image_"+image + '">Label</label><p id="' + "p_image_"+image +'"></p>\
        <textarea name="image_label" id="' + "image_label_"+image + '" style="display: none;"></textarea></div>'
        image += 1        
        cd.innerHTML += file_input
        document.getElementById("id_title").value = value
        document.getElementById("id_author").value = type
    } 
    
    else{ 
        //title = document.getElementById("id_title")
        type = author.value
        console.log("type", type)
        value = title.value
        console.log('This shit', cd.getElementsByClassName('form-row')[cd.getElementsByClassName('form-row').length-1].getElementsByTagName('textarea')[0].name)
        body.innerHTML = body.value
        
        if (image>1 && cd.getElementsByClassName('form-row')[cd.getElementsByClassName('form-row').length-1].getElementsByTagName('textarea')[0].name != "spawn_body"){ /* the last widget is not of the body textarea*/
            text_id = "id_text_"+text
            text_input = '<div class="form-row field-body" id="' + "div_text_"+text + '"><div><label for="' + text_id + '">Body:</label><textarea name="spawn_body" cols="40" rows="10" class="vLargeTextField" id="' + text_id + '" style="display: inline;"></textarea>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type="button" value="remove" style="vertical-align: bottom;" onclick=remover(2,' + text_id + ');></div></div>'
            text += 1
            cd.innerHTML = cd.innerHTML + text_input
        }
        document.getElementById("id_title").value = value
        document.getElementById("id_author").value = type
    } 
}


function remover(mode, k){
    document.getElementById("div"+k.id.slice(2)).outerHTML = ""
}

function romero(tally){
    let input = document.getElementById("id_image_"+tally);
    console.log('Logger', input, tally)
    input.addEventListener("change", () => {
    if (input.files.length > 0) {
        let file = input.files[0];
        console.log("You chose", file.name);
        xc = document.getElementById("p_image_"+tally)
        xs = document.getElementById("span_image_"+tally)
        xz = document.getElementById("image_label_"+tally)
        xc.innerHTML = '<img src="/media/' + file.name + '" alt="' + file.name + '" >'    
        xz.innerHTML = file.name
        xs.innerHTML = file.name
        if (file.type) console.log("It has type", file.type);
        }
    });
    console.log('ROMERO')
}