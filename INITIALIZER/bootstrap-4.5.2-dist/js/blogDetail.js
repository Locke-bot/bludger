$(function(){
    offset = 20; // gotta change it both here and when calling the fuckin' filter
    var slide = $("#postComment");
    slide.hide();
    function user_logged_in(){
        if (slide.attr("authenticated") == undefined){
            var flash = $("<div>",{
                                "text": "You have to be logged in to comment",
                                "style": "background-color: rgb(221, 255, 221); color: #155724; padding: 10px 10px 10px 65px;; text-align: center;", 
            })
            flash.prependTo("body")
            window.setTimeout(function() {
                  flash.fadeTo(500, 0).slideUp(500, function(){
                      flash.remove(); 
                  });
            }, 5000);
            return false
        }
        return true
    }
    reply = $(".commentReply") 
    selectReply = document.getElementById("id_reply")
    options  = $("option") 
    x = $(".usercomment")
    y = $(".collapser")
    
    $("#comments").on("click", ".likeButton", function(){
        console.log("like button clicked")
        $this = $(this)    
        next = $this.next() // the label 
        list = next.html().split(" ") 
        $(".likeButton").prop("disabled", true)
        ajax = $.ajax({
            type: "POST",
            url: "{% url 'detail' blog.datetime_added.date blog.title %}", // blog title is unique too
            data: {"name": "likes", "status": $this.is(":checked"), "pk": $this.parent().parent().parent().find("textarea").attr("name"), "csrfmiddlewaretoken": csrf_token},
            success: function(response){
                    prev = Number(list[0])
                    $this.is(":checked")? prev+=1: prev-=1;
                    console.log("SHS", prev, list[0]);
                    prev > 1? prefix = "s": prefix="";
                    next.html(prev +" like"+prefix);
            }
        })     
        ajax.done(function(response){
                $(".likeButton").prop("disabled", false)
                console.log("Ajax Sucessful", $this.parent().parent().parent().find("textarea").attr("name"))
        })
    })
    
    y.on("click", function(){
        $this = $(this)
        parent = $this.parent() 
        text = $this.text()
        nest = parent.attr("nest")
        if (text.startsWith("see")){
            $this.text(text.replace("see", "collapse"))
            nextNest = parent.next().attr("nest")
            if (!(nextNest == undefined)){
                parent = parent.next()
                while (nest<nextNest){
                    if (nest == nextNest-1){
                        parent.attr("hide", 0) 
                    } 
                    else{
                        parent.attr("hide", parent.attr("hide")-1)
                    }
                    parent = parent.next()
                    nextNest = parent.attr("nest")
                    if (nextNest == undefined){ 
                        break;
                    }
                }
            }
        }
        else{ 
            nextNest = parent.next().attr("nest")
            console.log("nextNest", nest, nextNest) 
            if (!(nextNest == undefined)){
                parent = parent.next()
                while (nest<nextNest){
                    parent.attr("hide", parent.attr("hide")+1)
                    parent = parent.next()
                    nextNest = parent.attr("nest") 
                    if (nextNest == undefined){
                        break;
                    }
                } 
            }
            $this.text(text.replace("collapse", "see")) 
        }             
    })

    $("#addComment").on("click", function(){
        if (!user_logged_in()){
            return;
        }
        slide.css("margin-left", "0px") // contigency
        console.log("clicked", slide, slide.is(":visible")) 
        slide.insertBefore($(this))
        if (!slide.is(":visible")){
            slide.show()
        } 
        else{
            slide.hide() 
        }
    })
    $("#comments").on("click", ".commentReply", function(){ 
        if (!user_logged_in()){
            return; 
        }        
        $this = $(this)
        bv = $this.attr("style").indexOf(":")+1
        cv = $this.attr("style").indexOf("px") 
        num = Number($this.attr("style").slice(bv, cv))
        slide.css("margin-left", num+offset+"px") // increment its shift to the right by offset
        slide.insertAfter($this.next().next()) 
        if (!slide.is(":visible")){
            console.log("SHOW")
            slide.show() 
        }           
        else{
            console.log("HIDE")
            slide.hide() 
        }
    }) 
    $("#adder").on("click", function(){
        $this = $(this)
        
        text = $this.parent().find("textarea").val();
        console.log("nati", text.trim(), "j", text.trim()=="")
        if (text.trim()==""){
            console.log("NOthing dey")
            return
        }
        
        nest = Number($this.parent().parent().attr("nest")) + 1;
        step = 20;
        parent_id = Number($this.parent().parent().find("textarea").attr("name")) // wraps, doesn't give undefined at end of DOM
        isNaN(nest)? parent_id = "None": parent_id=parent_id;
        
        console.log("adder", nest, parent_id)
        
        $.ajax({
                type: 'POST',
                data: {'name': 'comment', 'parent_id': parent_id, 'text': text, 'csrfmiddlewaretoken': csrf_token},
                success: function(data){
                    isNaN(nest)? nest=0: true;
                
                    check_like = '<input type="checkbox" type="submit" class="likeButton">'
                    collapse_button = '<a role="button" style="margin-left: 10px" class="smallfont collapser"></a>'
                    reply_button = '<a role="button" style="margin-left: ' + nest*step + 'px" class="commentReply smallfont">Reply</a>';
                    
                    comment_specs = '<span style="margin-left: 10px" class="commentSpecs smallfont">\
                        &nbsp;<span class="dotfont">&centerdot;</span> \
                        <span class="author">' + data['username'] + '</span>&nbsp;&nbsp;\
                        <span class="dotfont">&centerdot;</span><span class="commentTime">' + data['time_added'] + '.</span>&nbsp;&nbsp;<span class="dotfont">\
                        &centerdot;</span> <span class="likes">'+ `${check_like}` + ' <span class="likelabel">0 like</span></span></span>';
                    
                    textarea = '<span hide=0 nest=' + nest + '><textarea disabled class="usercomment" cols="40" readonly name=' + data['pk'] + ' style="margin-left: ' + nest*step + 'px">' + text + '</textarea>' + reply_button + collapse_button + comment_specs + '</span>';
                    flash = $(textarea);
                    x = $this.parent().parent();
                    nest==0? flash.prependTo("#comments"): flash.insertAfter(x);
                    $this.parent().hide();
                    $this.parent().find("textarea").val(""); //reset textarea to ""
                }
        }).done(function(){ 
                console.log("Ajax jazzed successfully");
        }) 
    })
}) 
