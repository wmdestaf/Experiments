// ==UserScript==
// @name         artflow batch
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  improving artflow ux because they refuse to
// @author       wmdestaf
// @match        https://artflow.ai/
// @icon         https://www.google.com/s2/favicons?domain=artflow.ai
// @grant        none
// ==/UserScript==
var lock;
var front;
var most_recent_batch = ["easter egg"];
(function() {
    'use strict';

    function getRandomInt(max) {
        return Math.floor(Math.random() * max);
    }
    window.onbeforeunload = function(){
        //save anything as sessionstorage on reload
        localStorage.setItem("batchtext",$("#batch_txt").val())
        localStorage.setItem("saved",$("#save_txt").val())
        localStorage.setItem("savetmp",JSON.stringify(most_recent_batch))
    }

    
    //add a batch button
    let div = document.getElementsByClassName("input-group-append")[0]
    div.innerHTML += "<button id='batch_btn'>batch</button>"
    div.innerHTML += "<button id='save_btn'>save</button>"
    div.innerHTML += "<button id='save_qry'>save last</button>"
    div.innerHTML += "<label for='keep_btn'>Do Not Overwrite</label>"
    div.innerHTML += "<input type='checkbox' id='keep_btn'/>"
    $("#keep_btn").change(function() {
        if($(this).prop("checked")) localStorage.setItem("keep_status","true")
        else localStorage.removeItem("keep_status")
    });

    $(document).on('click', '#save_qry', function() {
        if(!most_recent_batch) return;
        let ptr = document.getElementById("save_txt")
        ptr.value += (ptr.value ? "\n" : "") + most_recent_batch.join("\n")
        let strs = ptr.value.split("\n")
        ptr.value = [...new Set(strs)].join("\n")
    });

    //save
    $(document).on('click', '#save_btn', async function() {
        let urls = Array.from(document.getElementsByClassName("card-img-top")).slice(0,6).map(x => x.src)
        for(let i = 0; i < urls.length; ++i) {
            //maybe some randomization...?
            setTimeout(() => { window.open(urls[i]) }, 2000 - (500 * (getRandomInt(4) - 2)));
        }
    });
    //add a textfield
    $("#empty_warning").before("<textarea id='batch_txt' cols='70' rows='12'></textarea>")
    //fill the textfield
    document.getElementById("batch_txt").value = localStorage.getItem("batchtext");
    //add another one
    $("#empty_warning").before("<textarea id='save_txt' cols='60' rows='12'></textarea>")
    document.getElementById("save_txt").value = localStorage.getItem("saved");
    most_recent_batch = JSON.parse(localStorage.getItem("savetmp"))

    //overwrite lock
    $("#keep_btn").prop("checked",localStorage.getItem("keep_status"))

    //fun
    function fire(n, inp) {
        document.getElementById("text_prompt").value = inp;
        enter_press_submit_prompt()
        document.title = "Processing: " + (n + 1) + "..."
    }

    const silly_msg = "¡imágenes listas!" //silly but fine

    if(localStorage.getItem("done") == 1) {
        localStorage.setItem("done",null)
        document.title = silly_msg
    }

    $(document.documentElement).mousemove(function() {
        if(document.title === silly_msg) document.title = 'Artflow';
    });


    var observer = new MutationObserver(function(mutations) {
        lock++;
        if(!(lock % 12)) { //WOW
            if(!front.length) {
                localStorage.setItem("done",1)
                location.reload()
            }
            else setTimeout(fire, 1000, Math.floor(lock / 12), front.shift())
        }
    });
    observer.observe(document.getElementById("btnSubmit_img_gen"), { attributes: true });

    $(document).on('click', '#batch_btn', async function() {
       let el = document.getElementById("batch_txt")
       let old = el.value

       if(!old) return;

       $("#keep_btn").css("disabled","true")
       let txt = old.split("\n");

       front = txt.slice(0,6);
       let back = txt.slice(6);

       //front may need to be preprocessed...
       let copy = []
       for(let string of front) {
           const splitter = /(\d+)\*(.*)$/;
           let match = string.match(splitter);
           if(!match) copy.push(string);
           else {
              for(let i = 0; i < parseInt(match[1]); ++i) {
                  copy.push(match[2]);
              }
           }
       }
       front = copy.slice(0,6)
       back = back.concat(copy.slice(6))

       //condense consecutive multiplicities of 'back'
       let ct = 1, counting = []
       for(let i = 0; i < back.length; ++i) {
          if(back[i] === back[i + 1]) ct++;
          else {
              counting.push([back[i], ct]);
              ct = 1;
          }
       }
       back = []
       for(let entry of counting) {
           back.push(entry[1] + "*" + entry[0]);
       }
       el.value = back.join("\n");

       if($("#keep_btn").prop("checked")) el.value = old
       $("#keep_btn").css("disabled","false")

       most_recent_batch = [...new Set(front)]
       lock = 0
       fire(0, front.shift())
    });
})();