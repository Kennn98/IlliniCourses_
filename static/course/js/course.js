$(document).ready(function(){
    var login = window.location.host + '/accounts/login/';

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var GPA_semester = document.getElementById('GPA_term').value;
    var all_semester = document.getElementById('semester_term').value;
    var termGPA = echarts.init(document.getElementById('termGPA'));
    var GPA_semester=GPA_semester.split(",");
    var all_semester=all_semester.split(",");
    for (num in all_semester) {
        all_semester[num] = all_semester[num].replace("[","")
        all_semester[num] = all_semester[num].replace("]","")
        all_semester[num] = all_semester[num].replace("'","")
        all_semester[num] = all_semester[num].replace("'","")
        all_semester[num] = all_semester[num].replace(" ","")
    }
    for (num in GPA_semester) {
        GPA_semester[num] = GPA_semester[num].replace("[","")
        GPA_semester[num] = GPA_semester[num].replace("]","")
        GPA_semester[num] = GPA_semester[num].replace("'","")
        GPA_semester[num] = GPA_semester[num].replace("'","")
        GPA_semester[num] = GPA_semester[num].replace(" ","")
    }
    var option1 = {
        title: {
            text: 'Average GPA By Term' 
        },
        tooltip: {},
        legend: {
            data: ['GPA']
        },
        xAxis: {
            data: all_semester,
        },
        yAxis: {},
        series: [{
            name: 'GPA',
            type: 'line',
            color:"blue",
            data: GPA_semester,
        }],
    };
    termGPA.setOption(option1);



    var name_ins = document.getElementById('name_ins').value;
    var GPA_ins = document.getElementById('GPA_ins').value;
    var proGPA = echarts.init(document.getElementById('proGPA'));
    var name_ins = name_ins.split(",");
    var GPA_ins = GPA_ins.split(",");
    for (num in GPA_ins) {
        GPA_ins[num] = GPA_ins[num].replace("[","")
        GPA_ins[num] = GPA_ins[num].replace("]","")
        GPA_ins[num] = GPA_ins[num].replace("'","")
        GPA_ins[num] = GPA_ins[num].replace("'","")
        GPA_ins[num] = GPA_ins[num].replace(" ","")
    }
    for (num in name_ins) {
        name_ins[num] = name_ins[num].replace("[","")
        name_ins[num] = name_ins[num].replace("]","")
        name_ins[num] = name_ins[num].replace("'","")
        name_ins[num] = name_ins[num].replace("'","")
        name_ins[num] = name_ins[num].replace(" ","")
    }
    var option2 = {
        title: {
            text: 'Average GPA By Instructor' 
        },
        tooltip: {},
        legend: {
            data: ['GPA']
        },
        xAxis: {
            data: name_ins,
            axisLabel: {
                interval: 0,
                rotate: 10,
            },
        },
        yAxis: {},
        series: [{
            name: 'GPA',
            type: 'bar',
            color:"blue",
            data: GPA_ins,
        }],
    };
    proGPA.setOption(option2);


    $('#workloadshow').jRange({
        from: -1,   				//滑块范围的初始值
        to: 10,    				//滑块范围的终止值
        step: 1,   				//设置步长
        width: 300, 			//进度条的宽度
        showScale: false,  		//是否显示滑块上方的数值标签
        isRange: false,     		//是否为选取范围
        disable:true,
    })
    

    $("#SUBB").click(function() {
        var workload = document.getElementById('workloadR').value;
        var Ratinginput = document.getElementById('Ratinginput').value;
        console.log(workload, Ratinginput)
        $.ajax({
            headers: {'X-csrftoken': csrftoken},
            url:'',
            type: 'POST',
            data: {
                "rating": Ratinginput,
                "workload": workload,
                "action": 'add',
            },
            traditional: true,
            success:function(data){
                if(data.reason == 'unauthenticated user') {
                    window.location.assign('http://' + login);
                }
                $('#ratingstar').rating('update', data.updated_rating);
                $('#WLO').jRange('setValue', data.updated_workload + '');
                var WLS1 = document.getElementById('WLS1');
                WLS1.innerText = data.updated_workload;
            }
        })

    });



    $("#workloadR").change(function() {
        var workload = document.getElementById('workloadR').value;
        var WLS = document.getElementById('WLS');
        WLS.innerText = workload;
    });


    $("#DELB").click(function() {
        $.ajax({
            headers: {'X-csrftoken': csrftoken},
            url:'',
            type: 'POST',
            data: {
                "action": 'delete',
            },
            traditional: true,
            success:function(data){
                console.log(data)
                if(data.reason == 'unauthenticated user') {
                    window.location.assign('https://' + login);
                }
                $('#ratingstar').rating('update', data.updated_rating);
                $('#WLO').jRange('setValue', data.updated_workload + '');
                var WLS1 = document.getElementById('WLS1');
                WLS1.innerText = data.updated_workload;
            }
        })
    });

    $('#WLO').jRange({
        from: 0,   				//滑块范围的初始值
        to: 10,    				//滑块范围的终止值
        step: 0.5,   				//设置步长
        width: 300, 			//进度条的宽度
        showScale: false,  		//是否显示滑块上方的数值标签
        showLabels: false,  		//是否显示滑块上方的数值标签
        disable: true,
    })


    $('#ratingstar').rating('refresh', {disabled: true, showClear: false, showCaption: true, stars:'10'});

    $(document).on('click', '.tag', function() {
        if (this.getAttribute('class') == "tag tagon") {
            this.setAttribute('class', 'tag tagoff');
            console.log(this.innerText);
            $.ajax({
                headers: {'X-csrftoken': csrftoken},
                url:'',
                type: 'POST',
                data: {
                    "action": 'dectagcount',
                    "tagcontent": this.innerText,
                },
                traditional: true,
                success:function(data){
                    $('#fretaglist').empty();
                    const fre = document.querySelector('#fretaglist');
                    for (item in data.most_freq_tags) {
                        const tag = document.createElement('div');
                        console.log(item)
                        tag.innerText = data.most_freq_tags[item].content;
                        if (data.most_freq_tags[item].selected == 0) {
                            tag.setAttribute('class', 'tag tagoff');
                        } else {
                            tag.setAttribute('class', 'tag tagon');
                        }
                        fre.append(tag);
                    }
                }
            })
            return;
        }
        this.setAttribute('class', 'tag tagon');
        console.log(this.innerText)
        $.ajax({
            headers: {'X-csrftoken': csrftoken},
            url:'',
            type: 'POST',
            data: {
                "action": 'inctagcount',
                "tagcontent": this.innerText,
            },
            traditional: true,
            success:function(data){
                if(data.reason == 'unauthenticated user') {
                    window.location.assign('https://' + login);
                }
                $('#fretaglist').empty();
                const fre = document.querySelector('#fretaglist');
                for (item in data.most_freq_tags) {
                    const tag = document.createElement('div');
                    console.log(item)
                    tag.innerText = data.most_freq_tags[item].content;
                    if (data.most_freq_tags[item].selected == 0) {
                        tag.setAttribute('class', 'tag tagoff');
                    } else {
                        tag.setAttribute('class', 'tag tagon');
                    }
                    fre.append(tag);
                }
            }
        })
    })



    $('#addtag').click(function() {
        var text = document.getElementById('text').value;
        if (text === "") {
            alert('Say what you want!')
        }
        const box = document.getElementById('addtaglist')
        const newtag = document.createElement('div');
        newtag.setAttribute('class', 'tag tagon');
        newtag.innerText = text;
        document.getElementById('text').value = '';
        $.ajax({
            headers: {'X-csrftoken': csrftoken},
            url:'',
            type: 'POST',
            data: {
                "action": 'inctagcount',
                "tagcontent": text,
            },
            traditional: true,
            success:function(data){
                if(data.reason == 'unauthenticated user') {
                    window.location.assign('https://' + login);
                }
                $('#fretaglist').empty();
                const fre = document.querySelector('#fretaglist');
                for (item in data.most_freq_tags) {
                    const tag = document.createElement('div');
                    tag.innerText = data.most_freq_tags[item].content;
                    if (data.most_freq_tags[item].selected == 0) {
                        tag.setAttribute('class', 'tag tagoff');
                    } else {
                        tag.setAttribute('class', 'tag tagon');
                    }
                    fre.append(tag);
                }
            }
        })
        box.append(newtag)
    })


    $('#refresh').click(function() {
        $.ajax({
            headers: {'X-csrftoken': csrftoken},
            url:'',
            type: 'POST',
            data: {
                "action": 'randtagrefresh',
            },
            traditional: true,
            success:function(data){
                $('#rantaglist').empty();
                const fre = document.querySelector('#rantaglist');
                for (item in data.rand_tags) {
                    const tag = document.createElement('div');
                    tag.innerText = data.rand_tags[item].content;
                    if (data.rand_tags[item].selected == 0) {
                        tag.setAttribute('class', 'tag tagoff');
                    } else {
                        tag.setAttribute('class', 'tag tagon');
                    }
                    fre.append(tag);
                }
            }
        })
    })

    



    $("#Ratinginput").rating({
        stars: "10"
    });

    $("#ratingstar").rating({
        stars: "10"
    });
    
});


function msgbox(n){
    document.getElementById('inputbox').style.display=n?'block':'none';     /* 点击按钮打开/关闭 对话框 */
}


function jump() {
    window.location.assign('https://' + window.location.host);
}



