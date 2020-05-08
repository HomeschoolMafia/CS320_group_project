document.addEventListener('DOMContentLoaded', ()=>{

    // Send user back to login page if they didn't sign in
    const username = localStorage.getItem('username');
    if (username == null){
      window.location = "/";
    }
  
    // Switch button active class when clicked
    $('.list-group .list-group-item.list-group-item-action').click(function(e) {
      $('.list-group .list-group-item.list-group-item-action.active').removeClass('active');
      var $this = $(this);
      if (!$this.hasClass('active')) {
          $this.addClass('active');
      }
      e.preventDefault();
    });
  
    // Connect to socket.io
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
  
    socket.on('connect', () => {
  
      // Automatically connect to general channel
      socket.emit('join',{"channel": "general", "username":username});
  
      // When a channel is clicked, connect to that channel
      document.querySelectorAll('.list-group-item').forEach(function(channel){
        channel.onclick = () =>{
          socket.emit('join',{"channel":channel.innerHTML, "username":username});
          return false;
        }
      });
  
      // When a message is sent, call 'send message' function from server
      document.querySelector('#send-message').onsubmit = () => {
        const message = document.querySelector('#m').value
        socket.emit('send message', {'message': message});
  
        // Clear message form
        document.querySelector('#m').value = "";
  
        return false;
      };
    });
  
    // Callback from server for sending messages
    socket.on('broadcast message', data =>{
      console.log(data);
      
    // Append message to list of messages
    const li = document.createElement('li');
    li.innerHTML = `${data.message}`;
    document.querySelector('#messages').append(li);

  });
});