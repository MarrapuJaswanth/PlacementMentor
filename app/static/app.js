const $=id=>document.getElementById(id);
function profile(){return {name:$("name").value,branch:$("branch").value,year:$("year").value,target_role:$("role").value,programming_languages:$("langs").value.split(",").map(x=>x.trim()),technologies:$("tech").value.split(",").map(x=>x.trim()).filter(Boolean),preparation_days:Number($("days").value)}}
function add(text,who){let d=document.createElement("div");d.className="msg "+who;d.innerHTML="<b>"+(who==="user"?"You":"PlacementMentor")+"</b><div>"+text.replace(/\n/g,"<br>")+"</div>";$("chat").appendChild(d);$("chat").scrollTop=$("chat").scrollHeight}
async function ask(text,mode="general"){add(text,"user");let r=await fetch("/api/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:text,profile:profile(),mode})});let x=await r.json();add(x.answer,"bot")}
function send(){let x=$("msg").value.trim();if(x){$("msg").value="";ask(x)}}
function roadmap(){ask("Create a personalized "+$("days").value+" day placement roadmap covering DSA, CS fundamentals, development, projects, aptitude, resume, technical interviews and HR.","roadmap")}
$("msg").addEventListener("keydown",e=>{if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();send()}})
add("Welcome! Enter your profile and ask me what you should learn for your placement.","bot")
