$(function(){
    var xhr;
    search = $('#blogSearch')
    search.on("focusin", function(){
        $this = $(this)
        $this.on("keyup", function(event){
            window.setTimeout(function(){
                // the setTimeout part is important, so as to allow the last pressed key to show up
                pos = search.position()
                top = pos.top
                left = pos.left
                height = search.height()
                width = search.outerWidth()
                totalTop = Number(pos.top) + Number(height) + 13
                try{
                    xhr.abort() // to avoid run up of ajax calls, don't need a timeout for debouncing yet.
                    newUl.remove()
                } catch(error){
                }    
                if (!$this.val().trim()){
                    var cv = {
                        'id': 'search_list',
                        'class': 'dropdown-menu show',
                        'aria-labelledby': "blogSearch",
                        'style': 'left: ' + top.left + 'px; ' + 'top: ' + totalTop +'px; ' + 'width: ' + width + 'px;',
                    }
                    newUl = $('<ul />', cv)                
                    $('<a />', {
                        "text": 'No search results',
                        "class": "dropdown-item",
                    }).appendTo(newUl);
                    newUl.insertAfter($('nav#top-nav')[0]) 
                    return 
                }
                xhr = $.ajax({
                    type: 'POST',
                    name: 'search',
                    data: {'name': 'search_blog', 'csrfmiddlewaretoken': csrf_token, 'search_text': $this.val().trim()},
                    success: function(data){
                            no_result = true; // guilty till proven innocent
                            $('#search_list').remove()
                            urls = data['urls']
                            var cv = {
                                'id': 'search_list',
                                'class': 'dropdown-menu show',
                                'aria-labelledby': "blogSearch",
                                'style': 'left: ' + top.left + 'px; ' + 'top: ' + totalTop +'px; ' + 'width: ' + width + 'px;',
                            }
                            newUl = $('<ul />', cv)                
                            searchs = data['search_results']
                            for (let i=0; i < searchs.length; i++){
                                no_result = false;
                                $('<a />', {
                                    "text": searchs[i],
                                    "href": urls[i],
                                    "class": "dropdown-item",
                                }).appendTo(newUl);
                            }
                        if (no_result){
                            $('<a />', {
                                "text": 'No search results',
                                "class": "dropdown-item",
                            }).appendTo(newUl);
                        }
                        newUl.insertAfter($('nav#top-nav')[0]) 
                    }
                })
            }, 0)
        })
    })
    $("article").on('click', function(){
        $('#search_list').remove()
    })
}) 
