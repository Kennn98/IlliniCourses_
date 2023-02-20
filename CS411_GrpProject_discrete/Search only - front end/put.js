const CRN = document.location.search.match(new RegExp("[\?\&]CRN=([^\&]+)", "i"))[1];
function getres() {
axios.get('http://dummy.restapiexample.com/api/v1/employees')
.then(res => {
    const element = res.data.data;
    document.querySelector('#courseTitle').innerText = 'Employee';
    const content = document.querySelector('#content');
    const newLi = document.createElement('li')
    for (let ind of element)
    { 
        const newLi = document.createElement('li');
        newLi.setAttribute('class', 'limen');
        newLi.innerText = 'employee' + ind.employee_name;
        content.append(newLi);
    }
})
.catch(err => {
    document.location.href ='404.html?CRN=' + CRN
})};
