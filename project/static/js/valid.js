// usernameError = document.getElementById("username-error")
// nameError = document.getElementById("name-error")
// emailError = document.getElementById("email-error")
// phonenumberError = document.getElementById("phonenumber-error")
// passwordeError = document.getElementById("password-error")
// repasswordError = document.getElementById("repassword-error")




var usernameError = document.getElementById("username-error");

function validateUsername() {
   
   
    var username = document.getElementById("username").value;
    document.getElementById("username-error").innerHTML="";
    document.getElementById("username").style.border = "2px solid green";

    if (username.length === 0) {

        const para = document.createElement('p')
        para.innerHTML ="Username is required";
        para.style.color= 'red';
        usernameError.appendChild(para)

        
        console.log(usernameError)
        return false;
    }
    if (username.length < 4) {
         const para = document.createElement('p')
        para.innerHTML ="Username atleast have 4 characters";
        para.style.color= 'red';
        usernameError.appendChild(para)

        
        console.log(usernameError)
        return false;
    }
    if (username.length > 10) {
        const para = document.createElement('p')
        para.innerHTML ="Username should be under 10 characters";
        para.style.color= 'red';
        usernameError.appendChild(para)

        
        console.log(usernameError)
        return false;
    }
    if (!/^[a-zA-Z]+$/.test(username)) {
        const para = document.createElement('p')
        para.innerHTML ="Name should not contain numbers";
        para.style.color= 'red';
        usernameError.appendChild(para)

        
        console.log(usernameError)
        return false;
    }
    usernameError.innerHTML = "";
    
    return true;
}
var nameError = document.getElementById("name-error")

function Validatename(){
    var name = document.getElementById("name").value;
    document.getElementById("name-error").innerHTML="";
    document.getElementById("name").style.border = "2px solid green";

    if (!/^[a-zA-Z]+$/.test(name)) {
        const para = document.createElement('p')
        para.innerHTML ="Name should only contain alphabets";
        para.style.color= 'red';
        nameError.appendChild(para)

        
        console.log(nameError)
        return false;
    }
    nameError.innerHTML = "";
    
    return true;


}
var emailError = document.getElementById("email-error")

function validateEmail(){
    var email = document.getElementById("email").value;
    document.getElementById("email-error").innerHTML="";
    document.getElementById("email").style.border = "2px solid green";

    
    if(email.length === 0){

        const para = document.createElement('p')
        para.innerHTML = "Email is required";
        para.style.color= 'red';
        emailError.appendChild(para)
        console.log(emailError)
        return false;

    }
    if(!email.match(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/)){
        const para = document.createElement('p')
        para.innerHTML = "Invalid email"
        para.style.color= 'red';
        emailError.appendChild(para)
        console.log(emailError)
        return false
    }
    emailError.innerHTML = ""
    return true;


}

var phonenumberError = document.getElementById("phonenumber-error");

function validatePhone() {
    var phonenumber = document.getElementById("phonenumber").value;
    document.getElementById("phonenumber-error").innerHTML = "";
    document.getElementById("phonenumber").style.border = "2px solid green";

    // Regular expression to check if the phone number contains only digits
    if (!/^\d+$/.test(phonenumber)) {
        const para = document.createElement('p');
        para.innerHTML = "Phone number should contain only digits (0-9)";
        para.style.color = 'red';
        phonenumberError.appendChild(para);

        console.log(phonenumberError);
        return false;
    }
    if (phonenumber.length != 10) {
        const para = document.createElement('p')
        para.innerHTML ="Phone number should have ten digits";
        para.style.color= 'red';
        phonenumberError.appendChild(para)

        
        console.log(phonenumberError)
        return false;
    }
    phonenumberError.innerHTML = ""
    return true;
}

var passwordeError = document.getElementById("password-error")

function validatepassword(){
    let password = document.getElementById("password").value;
    document.getElementById("password-error").innerHTML = "";
    document.getElementById("password").style.border = "2px solid green";

    if (password.length < 6) {
       const para = document.createElement('p')
       para.innerHTML ="Password atleast have 6 characters";
       para.style.color= 'red';
       passwordeError.appendChild(para)

       
       console.log(passwordeError)
       return false;
   }
   passwordeError.innerHTML = ""
   return true;

}
var repasswordError = document.getElementById("repassword-error")

function validateConfirmPassword() {
    const password = document.getElementById("password").value;
    const rePassword = document.getElementById("re-password").value;
    document.getElementById("repassword-error").innerHTML = "";
    document.getElementById("re-password").style.border = "2px solid green";

    if (password !== rePassword) {
        const para = document.createElement('p');
        para.innerHTML = "Passwords do not match";
        para.style.color = 'red';
        repasswordError.appendChild(para);

        console.log(repasswordError);
        return false;
    }

    repasswordError.innerHTML = "";
    return true;
}

// function submitForm(){
//     if((!validateUsername()) || (!Validatename()) || (!validateEmail()) || (validatePhone())|| (validatepassword())|| (validateConfirmPassword()) ){
//       submitError.innerHTML='please fill all fields'
//       return false;
//     }else{
//       alert('form submit successfully')
//     }
//   }





// ########################################################################
    // Validation for username
    // if (!/^[a-zA-Z]+$/.test(username)) {
    //     errorMsg += "Name should only contain letters.\n";
    // }
    // if (username.length < 4) {
    //     errorMsg += "Name should have at least 4 characters.\n";
    // }
    // if (username.length > 10) {
    //     errorMsg += "Username can have at most 10 characters.\n";
    // }

    // Validation for email
    // if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email)) {
    //     errorMsg += "Invalid Email.\n";
    // }

    // Validation for password
    // if (password.length < 6) {
    //     errorMsg += "Password must have at least 6 characters.\n";
    // }
    // if (password !== repassword) {
    //     errorMsg += "Passwords do not match.\n";
    // }

    // Validation for phone number
    // if (!/^\d{10}$/.test(phonenumber)) {
    //     errorMsg += "Phone number should have ten digits.\n";
    // }

    // Validation for name (address)
    // if (!/^[a-zA-Z]+$/.test(name)) {
    //     errorMsg += "Address should only contain alphabets.\n";
    // }

    // if (errorMsg !== "") {
    //     alert(errorMsg);
    //     return false; // Prevent form submission
    // }
    // return true;
     // Allow form submission if all checks pass


// ###########################################################################################################

