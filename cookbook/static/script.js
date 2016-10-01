$(document).ready(function() {

    /* Ajax login */
    $('form.login').submit(function(e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "login",
            data: $(this).serialize(),
            success: function(data) {
                if (data.code == 1) {
                    location.reload();
                } else {
                    alert('Incorrect username or password.');
                }
            }
        });
    });

    /* Ajax create user */
    $('form.create').submit(function(e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: 'createUser',
            data: $(this).serialize(),
            success: function(data) {
                if (data.code == 1) {
                    location.reload();
                } else {
                    alert('Username already taken');
                }
            }
        });
    });

    /* Ajax add ingredient */
    $('form.new-ingredient').submit(function(e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "addIngredient",
            data: $(this).serialize(),
            success: function(data) {
                if (data.code == 1) {
                    $('div#content').load('reloadContent');
                    $('#new-ingredients').modal('hide');
                    $('div.alert-success').html(data.message);
                    $('div.alert-success').fadeIn()
                        .css("display","inline-block")
                        .delay(2000).fadeOut();
                } else {
                    var formGroup = $('form.new-ingredient div#form-name');
                    formGroup.addClass('has-error');
                    if (!formGroup.children('span').length) {
                        formGroup.append('<span class="help-block">'+data.message+'</span>')
                    }
                }
            }
        });
    });

    /* Populate the edit-ingredient modal. */
    $('#content').on('click', 'tr.ingredient', function() {
        var editModal = $('#edit-ingredient');
        editModal.find('input.name').val($(this).attr('data-name'));
        editModal.find('input.id').val($(this).attr('id'));
        editModal.find('select.location').val($(this).attr('data-location'));
        editModal.find('input.purchase').val($(this).attr('data-purchase'));
        editModal.find('input.expiration').val($(this).attr('data-expiration'));
        editModal.find('button.delete').attr('id', $(this).attr('id'));
        editModal.modal('show');
    });

    /* Ajax update ingredient */
    $('form.edit-ingredient').submit(function(e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "updateIngredient",
            data: $(this).serialize(),
            success: function(data) {
                if (data.code == 1) {
                    $('div#content').load('reloadContent');
                    $('#edit-ingredient').modal('hide');
                    $('div.alert-success').html(data.message);
                    $('div.alert-success').fadeIn()
                        .css("display","inline-block")
                        .delay(2000).fadeOut();
                } else {
                    alert(data.message);
                }
            }
        });
    });

    /* Ajax delete ingredient */
    $('button.deleteIngredient').on('click', function() {
        $.ajax({
            type: 'POST',
            url: 'deleteIngredient',
            data: $('form.edit-ingredient').serialize(),
            success: function(data) {
                if (data.code == 1) {
                    $('div#content').load('reloadContent');
                    $('#edit-ingredient').modal('hide');
                    $('div.alert-success').html(data.message);
                    $('div.alert-success').fadeIn()
                        .css("display","inline-block")
                        .delay(2000).fadeOut();
                } else {
                    alert(data.message);
                }
            }
        });
    });

    /* Append additional ingredient and instruction inputs when typing. */
    $('#edit-recipe,#new-recipe').on('input',
        'input.last,textarea.last', function() {
        if (this.value) {
            $(this).removeClass('last');
            var next = $(this).clone();
            next.addClass('last');
            next.val('');
            $(this).parent().parent().append($('<li></li>').append(next));
        }
    });

    /* Ajax add recipe */
    $('form.new-recipe').submit(function(e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "addRecipe",
            data: $('form.new-recipe :input').filter(
                function(i,e){return e.value != ''}).serialize(),
            success: function(data) {
                if (data.code == 1) {
                    $('div#content').load('reloadContent');
                    $('#new-recipe').modal('hide');
                    $('div.alert-success').html(data.message);
                    $('div.alert-success').fadeIn()
                        .css("display","inline-block")
                        .delay(2000).fadeOut();
                } else {
                    alert(data.message);
                }
            }
        });
    });

    /* Populate the edit-recipe modal. */
    $('#content').on('click', 'button.edit-recipe', function() {
        $('#edit-recipe').load('loadRecipeModal', {id: this.id}, function() {
            $('#edit-recipe').modal('show');
        });
    });

    /* Ajax update recipe */
    $('#edit-recipe').on('submit', 'form.edit-recipe', function(e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "updateRecipe",
            data: $('form.edit-recipe :input').filter(
                function(i,e){return e.value != ''}).serialize(),
            success: function(data) {
                if (data.code == 1) {
                    $('div#content').load('reloadContent');
                    $('#edit-recipe').modal('hide');
                    $('div.alert-success').html(data.message);
                    $('div.alert-success').fadeIn()
                        .css("display","inline-block")
                        .delay(2000).fadeOut();
                } else {
                    alert(data.message);
                }
            }
        });
    });

    /* Ajax delete recipe */
    $('#edit-recipe').on('click', 'button.deleteRecipe', function() {
        $.ajax({
            type: 'POST',
            url: 'deleteRecipe',
            data: { id: this.id },
            success: function(data) {
                if (data.code == 1) {
                    $('div#content').load('reloadContent');
                    $('#edit-recipe').modal('hide');
                    $('div.alert-success').html(data.message);
                    $('div.alert-success').fadeIn()
                        .css("display","inline-block")
                        .delay(2000).fadeOut();
                } else {
                    alert(data.message);
                }
            }
        });
    });

    /* Apply tablesorter function to all tables. */
    $('table').tablesorter({
        emptyTo: 'bottom',
        sortList: [[1,0]]
    });

    /* Clicking on a recipe shows that recipe. */
    $('#content').on('click', 'tr.item', function() {
        $('div.recipe#r'+this.id).show().siblings().hide();
        $('.items tbody').children().removeClass('selected');
        $(this).addClass('selected');
    });

    /* CSRF */
    var csrftoken = Cookies.get('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});
