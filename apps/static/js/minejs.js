function checkfirst(){
    if(password.value.length<=6){
        pass1pan.innerText="密码请保证至少7位!"
        return false;
    }
    else{
        pass1pan.innerText=""
        return true;
    }

}

function checkpass(){
    var form1=document.getElementById("mainform")
    var pass1=form1.password.value
    var pass2=form1.password2.value
    if(pass1==pass2){
        passpan.innerText="";
        return true;
    }

    else{
        passpan.innerText="密码不一致!";
        return false;
    }
}

function shouldsubmit(){
    if(checkfirst()&& checkpass())
        return true;
    else
        return false;
}


