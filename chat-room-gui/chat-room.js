//let AZApp = document.registerElement("az-app");
class AZApp extends HTMLElement {

}
console.log(HTMLElement)
window.customElements.define("az-app", AZApp);

const model = {
  groups: new ListState([]),
  messages: new ListState([]),
  selected_group: new ItemState(undefined)
}

model.groups.onPush(function(item) {
  $("#nav-chat-tabs").append("<h3>" + item + "</h3>")
  console.log(item);
  console.log(model.groups.expose())
});

model.messages.onPush(function(item) {
  const paragraph = $('<p class="mb-0 primary-color">' + item.message + '</p>');
  const footer = $('<footer class="blockquote-footer primary-color">' + item.author + '</footer>');

  const blockquote = $('<blockquote class="message text-left blockquote"></blockquote>');
  blockquote.append(paragraph);
  blockquote.append(footer);

  //const message_block = $('<section></section>');
  //message_block.append(blockquote);

  const message_stack = $("#message-stack");
  message_stack.append(blockquote);
  message_stack.scrollTop(message_stack[0].scrollHeight);
})

$("#chat-message-maker-text").keyup(function(e) {
  if(e.key === "Enter") {
    const text_field = $("#chat-message-maker-text");
    if(text_field.val() === "") {
      return;
    } else {
      model.messages.push({
        message: text_field.val(),
        author: "gerg"
      });
      text_field.val("");
    }
  }
})

$("#new-chat-button").click(function() {
  model.groups.push("another new chat");
});


/*
for(let m of ["A", "B", "C", "D", "E", "F", "H", "I", "J", "K", "L", "M"]) {
  model.messages.push({author: "Greg", message: m});

}*/
