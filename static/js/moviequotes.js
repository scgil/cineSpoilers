var rh = rh || {}; //el namespace es rh de Rose-Hulman y and in this app is called mq because is moviequotes
rh.mq = rh.mq || {};

rh.mq.editing = false;

rh.mq.attachEventHandlers = function() {

    $("#insert-quote-modal").on("shown.bs.modal", function(){

        $("input[name=quote]").focus();
    });
};

rh.mq.enableButtons = function() {

     $("#toggle-edit").click( function () {
       if (rh.mq.editing)  {
           rh.mq.editing = false;
           $(".edit-actions").addClass("d-none");
           $(this).html("Editar");
       } else {
           rh.mq.editing = true;
           $(".edit-actions").removeClass("d-none");
           $(this).html("Hecho");
       }
    });
    $("#add-quote").click( function() {

        $("#insert-quote-modal .modal-title").html("Añadir un CineSpoiler");
        $("#insert-quote-modal button[type=submit]").html("Añadir CineSpoiler");

        $("#insert-quote-modal input[name=quote]").val("");
        $("#insert-quote-modal input[name=movie]").val("");
        $("#insert-quote-modal input[name=entity_key]").val("").prop("disabled", true);
    });

        $(".edit-movie-quote").click( function(){
        $("#insert-quote-modal .modal-title").html("Editar este CineSpoiler");
        $("#insert-quote-modal button[type=submit]").html("Editar CineSpoiler");

        quote = $(this).find(".quote").html();
        movie = $(this).find(".movie").html();
        entityKey = $(this).find(".entity-key").html();

        $("#insert-quote-modal input[name=quote]").val(quote);
        $("#insert-quote-modal input[name=movie]").val(movie);
        $("#insert-quote-modal input[name=entity_key]").val(entityKey).prop("disabled", false);
    });
        $(".delete-movie-quote").click( function(){

        entityKey = $(this).find(".entity-key").html();

        $("#delete-quote-modal input[name=entity_key]").val(entityKey);
    });
};

$(document).ready( function() {
    rh.mq.enableButtons();
    rh.mq.attachEventHandlers();
});






//$("#toggle-edit").click( function () {
//    $(".edit-actions").toggleClass("invisible")
//})