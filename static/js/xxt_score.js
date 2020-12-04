$(function(){
    var $mytable = $("#mytable")
    function get_data(){
        data = {}
        data.csrfmiddlewaretoken = csrf
        data.c = $("#c").val()
        $.ajax({
            type:'post',
            url:url,
            data:data,
            success:function(data){
                if (data.status == 0){
                    alert(data.error)
                }else{
                    all_data = data.data
                    if (all_data){window.location.href = error_page;}
                    for (i in all_data){
                        stu_data = all_data[i]
                        var $tr = $("<tr></tr>")
                        var $th_name = $("<th>"+ stu_data['name'] +"</th>")
                        var $td_title = $("<td>" + stu_data['title'] +"</td>")
                        var $td_markperson = $("<td>" + stu_data['markPerson'] +"</td>")
                        var $td_total = $("<td>" + stu_data['total'] +"</td>")
                        var $td_score = $("<td>" + stu_data['score'] +"</td>")
                        $th_name.attr('scope','row')
                        $th_name.attr('abbr','Model')
                        $th_name.addClass('spec')
                        $tr.append($th_name)
                        $tr.append($td_title)
                        $tr.append($td_markperson)
                        $tr.append($td_total)
                        $tr.append($td_score)
                        $mytable.append($tr)
                    }
                }
            },
            error:function(xhr){

            }
        })
    }
    get_data()

})
















