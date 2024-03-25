function TypeWriter(reportText, paragraphId, speed) {
    const paragraph = document.getElementById(paragraphId);
    let index = 0;

    function typeWriter() {
        if (index < reportText.length) {
            paragraph.textContent += reportText.charAt(index);
            index++;
            setTimeout(typeWriter, speed);
        }
    }

    typeWriter();
}
