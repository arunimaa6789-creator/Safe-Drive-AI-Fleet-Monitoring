let fatigueData = []

const ctx = document.getElementById("fatigueChart")

const fatigueChart = new Chart(ctx, {

type:"line",

data:{
labels:[],
datasets:[{
label:"Fatigue Level",
data:fatigueData,
borderColor:"#00bfff",
backgroundColor:"rgba(0,191,255,0.2)",
tension:0.4,
fill:true
}]
},

options:{
scales:{
y:{
beginAtZero:true,
max:100
}
}
}

})


function updateChart(level){

let value = 0

if(level==="LOW") value=20
if(level==="HIGH") value=100

fatigueChart.data.labels.push(new Date().toLocaleTimeString())

fatigueChart.data.datasets[0].data.push(value)

if(fatigueChart.data.labels.length>10){
fatigueChart.data.labels.shift()
fatigueChart.data.datasets[0].data.shift()
}

fatigueChart.update()

}


function updateDashboard(){

fetch("/status")

.then(res=>res.json())

.then(data=>{

document.getElementById("driver-status").innerText=data.driver_status

document.getElementById("fatigue-level").innerText=data.fatigue_level

document.getElementById("alert").innerText=data.alert

document.getElementById("fleet-risk").innerText=data.fleet_risk

let fatigueFill=document.getElementById("fatigue-fill")

let score=100

if(data.fatigue_level==="LOW"){

fatigueFill.style.width="25%"
score=100

}

if(data.fatigue_level==="HIGH"){

fatigueFill.style.width="100%"
fatigueFill.style.background="#ff4444"
score=40

}

document.getElementById("safety-score").innerText=score+"%"

updateChart(data.fatigue_level)

})

}

setInterval(updateDashboard,2000)


function updateTime(){

let now=new Date()

document.getElementById("time").innerText=now.toLocaleTimeString()

}

setInterval(updateTime,1000)