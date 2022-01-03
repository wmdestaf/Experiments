// ==UserScript==
// @name         TTtH
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  uncensor 'censored' words from the most garbage censor engine I've seen in my entire life
// @author       wmdestaf
// @match        https://novelfull.com/the-tutorial-is-too-hard/*
// @icon         https://www.google.com/s2/favicons?domain=novelfull.com
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    /**
        While it's not strictly necessary to store the 'bad words' in a stateful manner,
        another goal of this software is to help 'reverse-engineer' the list of words
        which has been used in the aformentioned filter - with the ultamite result
        being the creation of a precomputed table to remove any visible preprocessing
        lag at all, via string replacing without the use of a regex engine entirely.
    */

    //As the software is self-learning, load in what we already know
    let badwords = JSON.parse(localStorage.getItem('badwords')) ?? [];

    //Then, make a first pass to discover any novel bad words
    const censor_find = /((\w\.){2,}\w)/gm; //For example, 'the titanic' appears as 'the t.i.tanic'

    for(let p of document.getElementsByTagName("p")) {
        let matches = p.innerHTML.matchAll(censor_find);
        for(const match of matches) {
            let badword = match[0].split(".").join("");
            if(!badwords.includes(badword)) { badwords.push(badword); } //only store unique
        }
    }

    //Finally, remove all of the 'bad words' with their actual equivalents
    for(let p of document.getElementsByTagName("p")) {
        for(let w of badwords) {
            //first, detect if the word should instead be capitalzed
            let cap = w[0].toUpperCase() + w.slice(1);
            let cap_regex = new RegExp('(?:^|“|([\.\?!] ))(' + w.split("").join('\.') + ")","gm");
            p.innerHTML = p.innerHTML.replaceAll(cap_regex, "$1"+cap);

            //otherwise, default to lowercase
            p.innerHTML = p.innerHTML.replaceAll(w.split("").join('.'),w);
        }
    }

    //Save back our list, in case we learned anything new!
    localStorage.setItem('badwords',JSON.stringify(badwords));
})();