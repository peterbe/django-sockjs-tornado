var Chat = (function() {
  var _socket;

  function init(socket) {
    _socket = socket;

    $('form').submit(function() {
      var name = $.trim($('input[name="name"]').val());
      var message = $.trim($('input[name="message"]').val());
      if (!name.length) {
        alert("No name :(");
      } else if (!message.length) {
        $('input[name="message"]').focus();
      } else {
        _socket.send_json({name: name, message: message});
        $('input[name="message"]').val('');
        $('input[name="message"]').focus();
      }
      return false;
    });

  }

  return {
     init: init
  };

})();

SockJS.prototype.send_json = function(data) {
  this.send(JSON.stringify(data));
};

var initsock = function(callback) {
  sock = new SockJS('http://' + SOCK.host + ':' + SOCK.port + '/' + SOCK.channel);

  sock.onmessage = function(e) {
    //console.log('message', e.data);
    var data = e.data;
    if (data.message && data.name) {
      var out = $('#out');
      $('<span>')
        .addClass('date')
        .text(data.date)
        .appendTo(out);
      $('<p>')
        .append($('<strong>').text(data.name + ': '))
        .append($('<span>').text(data.message))
        .appendTo(out);
      out.scrollTop(out.scrollTop() + 1000);
    }
  };

  sock.onclose = function() {
    console.log('closed :(');
  };

  sock.onopen = function() {
    console.log('open');
    if (sock.readyState !== SockJS.OPEN) {
      throw "Connection NOT open";
    }
    callback(sock);
  };

};


$(function() {
  initsock(function(socket) {
    Chat.init(socket);
  });
});
