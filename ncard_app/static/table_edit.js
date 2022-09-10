function deleteRow(btn) {
    var row = btn.parentNode.parentNode;
    row.parentNode.removeChild(row);
    };

$(document).ready(function(){
    $(document).on('dblclick',".editable",function(){
        var value=$(this).text();
        var input="<input type='text' class='input-data' value='"+value+"' class='form-control'>";
        $(this).html(input);
        $(this).removeClass("editable")
    });

    $(document).on("blur",".input-data", function(){
        var value=$(this).val();
        var td=$(this).parent("td");
        $(this).remove();
        td.html(value);
        td.addClass("editable");
        var type=td.data("type");
        sendToServer(td.data("id"),value, type);
    });

    $(document).on("keypress",".input-data", function(e){
        var key=e.which;
        if(key==13){
            var value=$(this).val();
            var td=$(this).parent("td");
            $(this).remove();
            td.html(value);
            td.addClass("editable");
            var type=td.data("type");
            sendToServer(td.data("id"),value,type);
        }
    });

    function sendToServer(id,value,type){
        console.log(id);
        console.log(value);
        console.log(type);
        $.ajax({
            url:"http://localhost:8000/save_people",
            type:"POST",
            data:{id:id,type:type,value:value},
        })
        .done(function(response){
            console.log(response);
        })
        .fail(function(){
            console.log("Error Occured");
        });
    }
});