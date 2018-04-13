/**
 * Created by vv on 12.04.18.
 */


function selectGroups() {

 $.ajax({
			url : '/groups/get/all',
			type : 'GET',
            dataType: 'json',
			success: function(res){
				var div = $('<div>')
                    .attr('class', 'form-group')
                    .append($('<lable>')
                        .attr('for', 'sel').text('Група')
        .append(
            $('<select>').attr('class',"form-control").attr('id',"sel"))
                    );

				var option = $('<option>');


				var module = '';

				$.each(res,function(index, value){
					module = $(option).clone();
					$(module).attr('id', index).text(':0');
					$(div).find('select').append(module);

				});
                $('#slectGroup').append(div);
			},
			error: function(error){
				console.log(error);
			}
		});

}


$('#add-student').click(function () {
            $.confirm({
                title: 'Додати студента',
                theme: 'material',
                content: function selectGroups() {

 $.ajax({
			url : '/groups/get/all',
			type : 'GET',
            dataType: 'json',
			success: function(res){
				var div = $('<div>')
                    .attr('class', 'form-group')
                    .append($('<lable>')
                        .attr('for', 'sel').text('Група')
        .append(
            $('<select>').attr('class',"form-control").attr('id',"sel"))
                    );

				var option = $('<option>');


				var module = '';

				$.each(res,function(index, value){
					module = $(option).clone();
					$(module).attr('id', index).text(':0');
					$(div).find('select').append(module);

				});
                $(this).append(div);
			},
			error: function(error){
				console.log(error);
			}
		});

}
/*                '<form  id="add-res">'+
                '<fieldset>'+
                    '<div class="panel panel-primary panel-heading">'+
                        '<legend><h2>Студент</h2></legend>'+
                        '<div class="panel-title">Прізвище</div>'+
                        '<input type="text" class="panel-body" name="last_name" value="">'+
                        '<br>'+
                        '<div class="panel-title">Імя</div>'+
                        '<input type="text" class="panel-body" name="first_name" value="">'+
                        '<br>'+
                        '<div class="panel-title">По-батькові</div>'+
                        '<input type="text" class="panel-body" name="middle_name" value="">'+
                        '<br>'+
                        '<div id="selectGroup">Група</div>'+
                        + selectGroups()+
                        '<select name="groups">'+
                        '<option value="volvo">Volvo</option>'+
                        '<option value="saab">Saab</option>'+
                        '<option value="fiat" selected>Fiat</option>'+
                        '<option value="audi">Audi</option>'+
                        '</select>'+
                        '<br>'+
                    '</div>'+
                '</fieldset>'+
        '</form>'*/,
                buttons: {
                    'Додати': {

                        action: function () {
                        $.ajax({
                            url: '/add/student',
                            type: 'POST',
                            data: $('#add-res').serialize(),
                            success: function (response) {
                            localStorage.setItem('result', response.success);
                                if(response.success){
                                    localStorage.setItem('message', 'Студента додано успішно');
                                    location.reload();
                                }
                                else{
                                    localStorage.setItem('message', 'Пробеми з додаванням');
                                    location.reload();
                                }
                        }
                        });
                    }
                    },
                    'Відмінити': {

                        action: function () {
                        toastr.info('Create Cancelled');
                    }}
                }
            });
  });


$('#add-kurator').click(function () {
            $.confirm({
                title: 'Додати куратора',
                theme: 'material',
                content:
                '<form  id="add-res">'+
                '<fieldset>'+
                    '<div class="panel panel-primary panel-heading">'+
                        '<legend><h2>Куратор</h2></legend>'+
                        '<div class="panel-title">Прізвище</div>'+
                        '<input type="text" class="panel-body" name="last_name" value="">'+
                        '<br>'+
                        '<div class="panel-title">Імя</div>'+
                        '<input type="text" class="panel-body" name="first_name" value="">'+
                        '<br>'+
                        '<div class="panel-title">По-батькові</div>'+
                        '<input type="text" class="panel-body" name="middle_name" value="">'+
                        '<br>'+
                    '</div>'+
                '</fieldset>'+
        '</form>',
                buttons: {
                    'Додати': {

                        action: function () {
                        $.ajax({
                            url: '/add/kurator',
                            type: 'POST',
                            data: $('#add-res').serialize(),
                            success: function (response) {
                            localStorage.setItem('result', response.success);
                                if(response.success){
                                    localStorage.setItem('message', 'Куратора додано успішно');
                                    location.reload();
                                }
                                else{
                                    localStorage.setItem('message', 'Пробеми з додаванням');
                                    location.reload();
                                }
                        }
                        });
                    }
                    },
                    'Відмінити': {

                        action: function () {
                        toastr.info('Create Cancelled');
                    }}
                }
            });
  });

$('#add-group').click(function () {
            $.confirm({
                title: 'Додати групу',
                theme: 'material',
                content:
                '<form  id="add-res">'+
                '<fieldset>'+
                    '<div class="panel panel-primary panel-heading">'+
                        '<legend><h2>Група</h2></legend>'+
                        '<div class="panel-title">Назва групи</div>'+
                        '<input type="text" class="panel-body" name="group_name" value="">'+
                        '<br>'+
                    '</div>'+
                '</fieldset>'+
        '</form>',
                buttons: {
                    'Додати': {

                        action: function () {
                        $.ajax({
                            url: '/add/group',
                            type: 'POST',
                            data: $('#add-res').serialize(),
                            success: function (response) {
                            localStorage.setItem('result', response.success);
                                if(response.success){
                                    localStorage.setItem('message', 'Групу додано успішно');
                                    location.reload();
                                }
                                else{
                                    localStorage.setItem('message', 'Пробеми з додаванням');
                                    location.reload();
                                }
                        }
                        });
                    }
                    },
                    'Відмінити': {

                        action: function () {
                        toastr.info('Create Cancelled');
                    }}
                }
            });
  });
