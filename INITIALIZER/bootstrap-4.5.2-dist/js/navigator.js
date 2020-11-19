$(function(){
    search = $('#blogSearch')
    console.log(search)
    search.on("focusin", function(){
        $this = $(this)
        $this.on("keypress", function(){
            window.setTimeout(function(){
                // the setTimeout part is very important, so as to allow the last pressed key to show up
                //console.log('ddf', $this.val().trim())
                if (!$this.val().trim()){
                    return
                }
                $.ajax({
                    type: 'POST',
                    name: 'search',
                    data: {'name': 'search_blog', 'csrfmiddlewaretoken': csrf_token, 'search_text': $this.val()},
                    success: function(data){
                            no_result = true; // guilty till proven innocent
                            console.log(search.length, 'Ajax  is a jazz navigator')  
                            $('#search_list').remove()
                            pos = search.position()
                            top = pos.top
                            left = pos.left
                            height = search.height()
                            width = search.outerWidth()
                            totalTop = Number(pos.top) + Number(height) + 13
                            var cv = {
                                'id': 'search_list',
                                'class': 'dropdown-menu show',
                                'aria-labelledby': "blogSearch",
                                'style': 'left: ' + top.left + 'px; ' + 'top: ' + totalTop +'px; ' + 'width: ' + width + 'px;',
                            }
                            newUl = $('<ul />', cv)
                            urls = data['urls']
                            searchs = data['search_results']
                            for (let i=0; i < searchs.length; i++){
                                no_result = false;
                                $('<a />', {
                                    "text": searchs[i],
                                    "href": urls[i],
                                    "class": "dropdown-item",
                                }).appendTo(newUl);
                            }
                        console.log("newUi", newUl, newUl.html(), $("#blogSearch").position(), left, pos.top)
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
        console.log('remove')
        $('#search_list').remove()
    })
}) 
