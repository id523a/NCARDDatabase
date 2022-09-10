function deleteRow(btn) {
    var row = btn.parentNode.parentNode;
    row.parentNode.removeChild(row);
    };

function getCookie(name) {
    // Code from: https://docs.djangoproject.com/en/4.1/howto/csrf/#using-csrf
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

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
        const formData = new FormData();
        formData.append("id", id)
        formData.append("type", type)
        formData.append("value", value)
        fetch("http://localhost:8000/save_people", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: formData
        })
        .then(function(response){
            console.log(response);
        })
        .catch(function(error){
            console.log("Error Occured");
        });
    }
});