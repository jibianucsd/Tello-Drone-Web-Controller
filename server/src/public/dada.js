document.addEventListener("DOMContentLoaded", (event) => {

    var da = 'http://localhost:8000/get_telemetry';
    setInterval(function(){
        fetch(da)
        .then(response=>response.json())
        .then(function(response){
            console.log(response)
            for(let key in response){
                document.getElementById(key).innerHTML = response[key];
            }
        })
    }, 3000);

    document.querySelector('#pmode').addEventListener("submit",function(e){
        var cmd = document.getElementById("txt").value;
        const d = {ida: cmd};
        console.log(cmd)
        fetch('/flight_plan',
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(d),
        }).then(response => response.json())
        e.preventDefault();
    })

    document.querySelector('#cmd1').addEventListener("submit",function(e){
        var mag = "";
        var takeoff = document.getElementById("takeoff").id;
        geturl(takeoff, mag)
        e.preventDefault();
    })
    document.querySelector('#cmd2').addEventListener("submit",function(e){
        var mag = document.getElementById("mag").value;
        var up = document.getElementById("up").id;
        geturl(up, mag)
        e.preventDefault();
    })
    document.querySelector('#cmd3').addEventListener("submit",function(e){
        var mag = document.getElementById("mag").value;
        var forward = document.getElementById("forward").id;
        geturl(forward, mag) 
        e.preventDefault();
    })
    document.querySelector('#cmd4').addEventListener("submit",function(e){
        var mag = document.getElementById("mag").value;
        var ccw = document.getElementById("ccw").id;
        geturl(ccw, mag) 
        e.preventDefault();
    })
    document.querySelector('#cmd5').addEventListener("submit",function(e){
        var mag = document.getElementById("mag").value;
        var cw = document.getElementById("cw").id;
        geturl(cw, mag) 
        e.preventDefault();
    })
    document.querySelector('#cmd6').addEventListener("submit",function(e){
        var mag = document.getElementById("mag").value;
        var back = document.getElementById("back").id;
        geturl(back, mag) 
        e.preventDefault();
    })
    document.querySelector('#cmd7').addEventListener("submit",function(e){
        var mag = document.getElementById("mag").value; 
        var down = document.getElementById("down").id;
        geturl(down, mag) 
        e.preventDefault();
    })
    document.querySelector('#cmd8').addEventListener("submit",function(e){
        var mag = "";
        var land = document.getElementById("land").id;
        geturl(land, mag)
        e.preventDefault();
    })

    function geturl(act, m){
        var ms = '/'+m;
        if(m != ""){
            var url = 'http://localhost:8000/drone_command/'+act+ms;
        }
        else{
            var url = 'http://localhost:8000/drone_command/'+act;
        }
        fetch(url)
            .then(response=>response.json())
    }
});