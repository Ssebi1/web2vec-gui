document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".extractor").forEach(extractor => {
        extractor.addEventListener("click", function () {
            let pageResult = this.closest(".page-result");

            pageResult.querySelectorAll(".page-result-result").forEach(result => {
                result.style.display = "none";
            });

            pageResult.querySelectorAll(".extractor").forEach(extr => {
                extr.classList.remove("active-extractor");
            });

            let extractorName = this.id.split("-")[0];
            let pageUrl = this.id.split("-").slice(1).join("-");
            let resultDiv = document.getElementById(`result-${extractorName}-${pageUrl}`);

            if (resultDiv) {
                resultDiv.style.display = "block";
            }

            this.classList.add("active-extractor");
        });
    });

    document.querySelectorAll(".page-result-header").forEach(header => {
        header.addEventListener("click", function () {
            let pageResult = this.parentElement;
            let content = pageResult.querySelector(".page-result-content");

            document.querySelectorAll(".page-result-content").forEach(otherContent => {
                if (otherContent !== content) {
                    otherContent.style.display = "none";
                }
            });

            content.style.display = (content.style.display === "none" || content.style.display === "") ? "flex" : "none";
        });
    });

    document.querySelectorAll(".page-result").forEach(pageResult => {
        let extractors = pageResult.querySelectorAll(".extractor");

        if (extractors.length > 0) {
            extractors[0].classList.add("active-extractor");
            extractors[0].click();
        }
    });
});
