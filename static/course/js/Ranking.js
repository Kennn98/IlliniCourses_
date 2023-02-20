var lo = 0;
var hi = 20;
var BGEL = [];
var BSUBL = [];
var avgratinglo = 0;
var avgratinghi = 10;
var avgworkloadlo = 0;
var avgworkloadhi = 10;
var ratingkeyword = [];
var ratingorder = [];
var rsort = [];
var rsl = []
var wsort = [];
var wsl = []
$(document).ready(function(){


    $(".submit").change(function() {
        lo = 0;
        hi = 20;
        var GE = document.getElementsByName("GE");
        var SUB = document.getElementsByName("SUB");
        BGEL = [];
        BSUBL = [];
        for(var i = 0; i < GE.length; i++){
            if(GE[i].checked == true){
                BGEL.push(GE[i].id);
            }
        }
        for(var i = 0; i < SUB.length; i++){
            if(SUB[i].checked == true){
                BSUBL.push(SUB[i].id);
            }
        }
        $.ajax({
            url:'/ranking',
            type: 'get',
            data: {
                "isdataonly":'True',
                "gened": BGEL,
                "subject": BSUBL,
                "lo": lo,
                "hi": hi,
                'avgratinglo': avgratinglo,
                'avgratinghi': avgratinghi,
                'avgworkloadlo': avgworkloadlo,
                'avgworkloadhi': avgworkloadhi,
                'ratingkeyword': ratingkeyword,
                'ratingorder': ratingorder,
            },
            traditional: true,
            success:function(data){
                reapp(data)
            }
        })
    });

   
    $('#Ratinginput').jRange({
        from: 0,   				//滑块范围的初始值
        to: 10,    				//滑块范围的终止值
        step: 1,   				//设置步长
        width: 150, 			//进度条的宽度
        showScale: false,  		//是否显示滑块上方的数值标签
        isRange: true,     		//是否为选取范围
        ondragend: function(e){    //滑块范围改变时触发的方法
            lo = 0;
            hi = 20;
            avgratinglo = e[0];
            avgratinghi = e[2];
            if (e[3] == 0) {
                avgratinghi = e[2] + e[3];
            }
            $.ajax({
                url:'/ranking',
                type: 'get',
                data: {
                    "isdataonly":'True',
                    "gened": BGEL,
                    "subject": BSUBL,
                    "lo": lo,
                    "hi": hi,
                    'avgratinglo': avgratinglo,
                    'avgratinghi': avgratinghi,
                    'avgworkloadlo': avgworkloadlo,
                    'avgworkloadhi': avgworkloadhi,
                    'ratingkeyword': ratingkeyword,
                    'ratingorder': ratingorder,
                },
                traditional: true,
                success:function(data){
                    reapp(data)
                }
            })
        }
    })
    
	
    $('#Ratinginput').jRange('setValue', '0, 10');

    $('#workloadinput').jRange({
        from: 0,   				//滑块范围的初始值
        to: 10,    				//滑块范围的终止值
        step: 1,   				//设置步长
        width: 150, 			//进度条的宽度
        showLabels: true,  		//是否显示滑动条下方的尺寸标签
        showScale: false,  		//是否显示滑块上方的数值标签
        isRange: true,     		//是否为选取范围
        ondragend: function(e){    //滑块范围改变时触发的方法
            lo = 0;
            hi = 20;
            avgratinglo = e[0];
            avgratinghi = e[2];
            if (e[3] == 0) {
                avgratinghi = e[2] + e[3];
            }
            $.ajax({
                url:'/ranking',
                type: 'get',
                data: {
                    "isdataonly":'True',
                    "gened": BGEL,
                    "subject": BSUBL,
                    "lo": lo,
                    "hi": hi,
                    'avgratinglo': avgratinglo,
                    'avgratinghi': avgratinghi,
                    'avgworkloadlo': avgworkloadlo,
                    'avgworkloadhi': avgworkloadhi,
                    'ratingkeyword': ratingkeyword,
                    'ratingorder': ratingorder,
                },
                traditional: true,
                success:function(data){
                    reapp(data)

                }
            })
        }
    })
	
    $('#workloadinput').jRange('setValue', '0, 10');


    $(document).on('click', '.rsort', function() {
        rsl = ["average_rating"];
        if (rsort[0] == 'DESC') {
            rsort = ['ASC'];
        } else {
            rsort = ['DESC'];
        }
        ratingkeyword = [].concat(rsl, wsl)
        ratingorder = [].concat(rsort, wsort)
        $.ajax({
            url:'/ranking',
            type: 'get',
            data: {
                "isdataonly":'True',
                "gened": BGEL,
                "subject": BSUBL,
                "lo": lo,
                "hi": hi,
                'avgratinglo': avgratinglo,
                'avgratinghi': avgratinghi,
                'avgworkloadlo': avgworkloadlo,
                'avgworkloadhi': avgworkloadhi,
                'ratingkeyword': ratingkeyword,
                'ratingorder': ratingorder,
            },
            traditional: true,
            success:function(data){
                reapp(data)
            }
        })
    })

    $(document).on('click', '.wsort', function() {
        wsl = ["average_workload"];
        if (wsort[0] == "ASC") {
            wsort = ['DESC'];
        } else {
            wsort = ["ASC"];
        }
        console.log(wsort)
        ratingkeyword = [].concat(wsl, rsl)
        ratingorder = [].concat(wsort, rsort)
        $.ajax({
            url:'/ranking',
            type: 'get',
            data: {
                "isdataonly":'True',
                "gened": BGEL,
                "subject": BSUBL,
                "lo": lo,
                "hi": hi,
                'avgratinglo': avgratinglo,
                'avgratinghi': avgratinghi,
                'avgworkloadlo': avgworkloadlo,
                'avgworkloadhi': avgworkloadhi,
                'ratingkeyword': ratingkeyword,
                'ratingorder': ratingorder,
            },
            traditional: true,
            success:function(data){
                reapp(data)
            }
        })
    })
});

function UP(){
    console.log(lo, hi);
    if (lo == 0) {
        alert('Cannot go up!')
        return;
    }
    lo = lo - 20;
    hi = hi - 20;
    $.ajax({
        url:'/ranking',
        type: 'get',
        data: {
            "isdataonly":'True',
            "gened": BGEL,
            "subject": BSUBL,
            "lo": lo,
            "hi": hi,
            'avgratinglo': avgratinglo,
            'avgratinghi': avgratinghi,
            'avgworkloadlo': avgworkloadlo,
            'avgworkloadhi': avgworkloadhi,
            'ratingkeyword': ratingkeyword,
            'ratingorder': ratingorder,
        },
        traditional: true,
        success:function(data){
            reapp(data)
        }
    });
};

function DOWN(){
    console.log(lo, hi);
    lo = lo + 20;
    hi = hi + 20;

    $.ajax({
        url:'/ranking',
        type: 'get',
        data: {
            "isdataonly":'True',
            "gened": BGEL,
            "subject": BSUBL,
            "lo": lo,
            "hi": hi,
            'avgratinglo': avgratinglo,
            'avgratinghi': avgratinghi,
            'avgworkloadlo': avgworkloadlo,
            'avgworkloadhi': avgworkloadhi,
            'ratingkeyword': ratingkeyword,
            'ratingorder': ratingorder,
        },
        traditional: true,
        success:function(data){
            var arr = Object.keys(data); 
            if (arr.length == 0) {
                lo = lo - 20;
                hi = hi - 20;
                alert('No more data!')
                return
            }
            reapp(data)

        }
    });


};


function isInteger(obj) {
    if (obj % 1 === 0){
        return obj;
    } else {
        return obj.toFixed(1)
    }
}


function reapp(data) {
    $("#Show").empty();
    const Show = document.querySelector('#Show');
    const table = document.createElement('table');
    table.setAttribute('class', 'table');
    table.innerHTML = "<caption><td class='TT'>Subject</td><td class='TT'>Number</td><td class='TT'>Rating<svg width='1em' height='1em' class='rsort' viewBox='0 0 16 16' class='bi bi-arrow-down-up' fill='currentColor' xmlns='http://www.w3.org/2000/svg'><path fill-rule='evenodd' d='M11.5 15a.5.5 0 0 0 .5-.5V2.707l3.146 3.147a.5.5 0 0 0 .708-.708l-4-4a.5.5 0 0 0-.708 0l-4 4a.5.5 0 1 0 .708.708L11 2.707V14.5a.5.5 0 0 0 .5.5zm-7-14a.5.5 0 0 1 .5.5v11.793l3.146-3.147a.5.5 0 0 1 .708.708l-4 4a.5.5 0 0 1-.708 0l-4-4a.5.5 0 0 1 .708-.708L4 13.293V1.5a.5.5 0 0 1 .5-.5z'/></svg></td><td class='TT'>Workload<svg width='1em' height='1em' class='wsort' viewBox='0 0 16 16' class='bi bi-arrow-down-up' fill='currentColor' xmlns='http://www.w3.org/2000/svg'><path fill-rule='evenodd' d='M11.5 15a.5.5 0 0 0 .5-.5V2.707l3.146 3.147a.5.5 0 0 0 .708-.708l-4-4a.5.5 0 0 0-.708 0l-4 4a.5.5 0 1 0 .708.708L11 2.707V14.5a.5.5 0 0 0 .5.5zm-7-14a.5.5 0 0 1 .5.5v11.793l3.146-3.147a.5.5 0 0 1 .708.708l-4 4a.5.5 0 0 1-.708 0l-4-4a.5.5 0 0 1 .708-.708L4 13.293V1.5a.5.5 0 0 1 .5-.5z'/></svg></td></caption>";
    for (i in data) {
        const text = document.createElement('tr');
        text.innerHTML = "<caption><td id='ST'>"+data[i]['subject']+"</td><td id='NT'><a href='/courses/"+data[i]['subject']+data[i]['number']+"'>"+data[i]['number']+"</a></td><td id='RT'>"+isInteger(data[i]['average_rating'])+"</td><td id='WLT'>"+isInteger(data[i]['average_workload'])+"</td></caption>";
        table.append(text)
    }
    Show.append(table)
}


function jump() {
    window.location.assign('http://' + window.location.host);
}