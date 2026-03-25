"use client"

import { useState } from "react"
import { Bar } from "react-chartjs-2"
import {
Chart as ChartJS,
CategoryScale,
LinearScale,
BarElement,
Title,
Tooltip,
Legend
} from "chart.js"

ChartJS.register(
CategoryScale,
LinearScale,
BarElement,
Title,
Tooltip,
Legend
)

export default function Home(){

const backend="http://127.0.0.1:8000"

const [labFile,setLabFile]=useState(null)
const [labResult,setLabResult]=useState(null)

const [prescriptionFile,setPrescriptionFile]=useState(null)
const [prescriptionResult,setPrescriptionResult]=useState(null)

const [question,setQuestion]=useState("")
const [answer,setAnswer]=useState("")
const [contextBuilt,setContextBuilt]=useState(false)

// LAB REPORT
const analyzeLab=async()=>{

const formData=new FormData()
formData.append("file",labFile)

const res=await fetch(`${backend}/analyze`,{
method:"POST",
body:formData
})

const data=await res.json()

setLabResult(data)

}

// PRESCRIPTION
const analyzePrescription=async()=>{

const formData=new FormData()
formData.append("file",prescriptionFile)

const res=await fetch(`${backend}/analyze_prescription`,{
method:"POST",
body:formData
})

const data=await res.json()

setPrescriptionResult(data)

}

// AI COPILOT
const askAI=async()=>{

const res=await fetch(`${backend}/ask`,{
method:"POST",
headers:{ "Content-Type":"application/json"},
body:JSON.stringify({question})
})

const data=await res.json()

setAnswer(data.answer)

}

// BUILD REPORT CONTEXT FOR AI
const buildContext=async()=>{

if(!labResult || !labResult.abnormalities){
alert("Please analyze a lab report first")
return
}

const abnormalitiesText = labResult.abnormalities && labResult.abnormalities.length > 0
? labResult.abnormalities.map(a=>`${a.test}: ${a.value}`).join(', ')
: "No abnormalities detected"

const riskScoreText = labResult.risk_score ? `${labResult.risk_score.score} (${labResult.risk_score.status})` : "Calculating"

const text = `Lab Report Summary: ${labResult.summary || "Analysis in progress"}. Abnormalities: ${abnormalitiesText}. Risk Score: ${riskScoreText}`

const res=await fetch(`${backend}/build_report_context`,{
method:"POST",
headers:{ "Content-Type":"application/json"},
body:JSON.stringify({text})
})

const data=await res.json()

if(data.message){
setContextBuilt(true)
alert("Report context built for AI copilot!")
}

}

// CHART DATA
const chartData = labResult && labResult.abnormalities && labResult.abnormalities.length > 0
? {
labels: labResult.abnormalities.map(a => a.test),
datasets: [{
label: "Lab Values",
data: labResult.abnormalities.map(a => a.value),
backgroundColor: "#3b82f6"
}]
}
: null


return(

<div style={{
padding:"40px",
background:"#f3f6fb",
color:"black",
minHeight:"100vh",
fontFamily:"Arial"
}}>

<h1 style={{fontSize:"36px"}}>AI Medical Intelligence Dashboard</h1>

<hr style={{margin:"20px 0"}}/>

{/* LAB REPORT */}

<div style={{
background:"white",
padding:"25px",
borderRadius:"10px",
marginBottom:"20px"
}}>

<h2>Upload Lab Report</h2>

<input type="file"
onChange={(e)=>setLabFile(e.target.files[0])}
/>

<br/><br/>

<button
style={{
padding:"10px 20px",
background:"#2563eb",
color:"white",
border:"none",
borderRadius:"6px"
}}
onClick={analyzeLab}
>
Analyze Report
</button>

<br/><br/>

{labResult &&(
<button
style={{
padding:"10px 20px",
background:"#dc2626",
color:"white",
border:"none",
borderRadius:"6px"
}}
onClick={buildContext}
>
Build AI Context
</button>
)}

{labResult &&(

<div style={{marginTop:"20px"}}>

<h3>Health Risk Score</h3>

<div style={{
background:"#ffe8e8",
padding:"15px",
borderRadius:"10px",
fontSize:"22px",
fontWeight:"bold"
}}>
{labResult.risk_score ? `${labResult.risk_score.score} - ${labResult.risk_score.status}` : "Calculating..."}
</div>

<h3 style={{marginTop:"20px"}}>Medical Summary</h3>

<p>{labResult.summary || "Analysis in progress..."}</p>

<h3>Critical Alerts</h3>

<ul>
{labResult.alerts && labResult.alerts.length > 0 ? (
  labResult.alerts.map((a,i)=>(
    <li key={i}>{a}</li>
  ))
) : (
  <li>No critical alerts detected.</li>
)}
</ul>

<h3>Possible Conditions</h3>

<ul>
{labResult.possible_conditions && labResult.possible_conditions.length > 0 ? (
  labResult.possible_conditions.map((d,i)=>(
    <li key={i}>{d}</li>
  ))
) : (
  <li>No conditions detected.</li>
)}
</ul>
{labResult.abnormalities && labResult.abnormalities.length === 0 && (
<p>No abnormalities detected in the report.</p>
)}
{chartData &&(

<div style={{marginTop:"30px"}}>

<h3>Abnormality Chart</h3>

<Bar data={chartData}/>

</div>

)}

</div>

)}

</div>


{/* PRESCRIPTION */}

<div style={{
background:"white",
padding:"25px",
borderRadius:"10px",
marginBottom:"20px"
}}>

<h2>Prescription Analyzer</h2>

<input
type="file"
onChange={(e)=>setPrescriptionFile(e.target.files[0])}
/>

<br/><br/>

<button
style={{
padding:"10px 20px",
background:"#2563eb",
color:"white",
border:"none",
borderRadius:"6px"
}}
onClick={analyzePrescription}
>
Analyze Prescription
</button>

{prescriptionResult &&(

<div style={{marginTop:"20px"}}>

<h3>Detected Medicines</h3>

<ul>
{prescriptionResult.medicines && prescriptionResult.medicines.length > 0 ? (
  prescriptionResult.medicines.map((m,i)=>(
    <li key={i}>{m}</li>
  ))
) : (
  <li>No medicines detected.</li>
)}
</ul>

<h3>Drug Interaction Warnings</h3>

<ul>
{prescriptionResult.interaction_warnings && prescriptionResult.interaction_warnings.length > 0 ? (
  prescriptionResult.interaction_warnings.map((w,i)=>(
    <li key={i}>{w}</li>
  ))
) : (
  <li>No interaction warnings.</li>
)}
</ul>

</div>

)}

</div>


{/* AI COPILOT */}

<div style={{
background:"white",
padding:"25px",
borderRadius:"10px"
}}>

<h2>AI Medical Copilot</h2>

{!contextBuilt &&(
<p style={{color:"red"}}>⚠️ Please analyze a lab report and build AI context first.</p>
)}

{contextBuilt &&(
<p style={{color:"green"}}>✅ Report context is ready for questions.</p>
)}

<input
type="text"
placeholder="Ask about your report..."
style={{
width:"70%",
padding:"10px",
marginRight:"10px"
}}
onChange={(e)=>setQuestion(e.target.value)}
/>

<button
style={{
padding:"10px 20px",
background:"#16a34a",
color:"white",
border:"none",
borderRadius:"6px"
}}
onClick={askAI}
>
Ask AI
</button>

{answer &&(

<div style={{
marginTop:"20px",
background:"#eef3ff",
padding:"15px",
borderRadius:"10px"
}}>

<h3>AI Response</h3>

<p>{answer}</p>

</div>

)}

</div>

</div>

)

}