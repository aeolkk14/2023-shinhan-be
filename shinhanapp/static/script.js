$(document).ready(function () {
    $(".list-group-item-action").click(function () {
        let product_id = $(this).attr('id');
        $.get("http://127.0.0.1:8000/product/" + product_id + "/")
            .then(function (result) {
                $("#detailModalTitle").text(result.title);
                $("#detailModalPrice").text(result.price);
                $("#detailModalContent").html(result.content);
                $("#detailModalLocation").text(result.location);
                $("#detailModalImage").attr("src", result.image);
                $("#detailModalUsername").text(result.username);
                $("#detailModal").modal("show");
            });
    });
});