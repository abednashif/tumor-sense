function TypeWriter(reportText, paragraphId, speed) {
    /* / - line break*/

    const paragraph = document.getElementById(paragraphId);
    let index = 0;

    function typeWriter() {
        if (index > reportText.length) return
        if(reportText.charAt(index) === '\/')
            paragraph.appendChild(document.createElement('br'))
        else
            paragraph.innerHTML += reportText.charAt(index);
        index++;
        setTimeout(typeWriter, speed);
    }

    typeWriter();
}
