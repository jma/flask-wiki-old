function markdownPreview(url) {
    var $form = $('form');
    var $inputs = $form.find('input, textarea, button');
    var $pre = $('#preview');
    var bodycontent = 'title: preview\n\n' + $form.find('textarea').val();
    $inputs.prop('disabled', true);
    $pre
        .removeClass('alert')
        .removeClass('alert-error')
        .html('Loading...');
    $.ajax({
        url: url,
        type: 'POST',
        data: { body: bodycontent },
        success: function (msg) {
            $pre.html(msg);
        },
        error: function (e) {
            console.log('error: ', e);
            $pre.addClass('alert').addClass('alert-error');
            $pre.html('There was a problem with the preview.');
        },
        complete: function () {
            $inputs.prop('disabled', false);
        }
    });
};

  // Add the following code if you want the name of the file appear on select
  $('.wiki-files .custom-file-input').on('change', function() {
    var form = $('form');
    form.submit();
  });

  // copy the markdown code in the clip board
  function copy(name, link) {
    var $temp = $('<div>');
    $('body').append($temp);
    $temp
      .attr('contenteditable', true)
      .html('![' + name + '](' + link + ' "' + name +'"' + ')')
      .select()
      .on('focus', function() {
        document.execCommand('selectAll', false, null);
      })
      .focus();
    document.execCommand('copy');
    $temp.remove();
    $('.wiki-files .toast').toast('show');
  };