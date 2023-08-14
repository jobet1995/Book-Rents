$(document).ready(function () {
    $("#new-book-form").submit(function (event) {
        event.preventDefault();

        var title = $("#title").val();
        var author = $("#author").val();
        var genre = $("#genre").val();
        var publicationYear = $("#publication-year").val();
        var isbn = $("#isbn").val();
        var totalCopies = $("#total-copies").val();
        var availableCopies = $("#available-copies").val();

        var newBook = {
            title: title,
            author: author,
            genre: genre,
            publication_year: publicationYear,
            ISBN: isbn,
            total_copies: totalCopies,
            available_copies: availableCopies
        };

        $.ajax({
            url: "/books",
            type: "POST",
            data: JSON.stringify(newBook),
            contentType: "application/json",
            success: function () {
                alert("Book added successfully!");
                $("#new-book-form")[0].reset();
            },
            error: function (error) {
                console.log(error);
                alert("Error adding book. Please try again.");
            }
        });
    });
});
