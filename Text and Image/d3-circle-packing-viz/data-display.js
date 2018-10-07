function extractReadableContent(data) {
  var content = {
    name: data.name,
    sentiment: data.sentiment,
    children: data.children.map((child) => {
      let childObj = {};
      childObj.name = child.name;
      childObj.sentiment = child.sentiment;
      if (child.url) childObj.url = child.url;
      return childObj;
    })
  }
  return content;
}

function populateFields(isActive, data) {
  var className = isActive ? 'primary' : 'secondary';
  var nameField = document.querySelector(`#name .${className}`);
  var sentimentField = document.querySelector(`#sentiment .${className}`);
  var childrenField = $(`#children .${className}`);

  
  nameField.innerHTML = data.name;
  sentimentField.innerHTML = data.sentiment;
  childrenField.JSONView(data.children);
  $('body').on('click', 'a', function(e) {
    e.target.target = '_blank';
  });
}

function displayHoverData(content) {
  var data = extractReadableContent(content);
  populateFields(0, data);
}

function displayActiveData(content) {
  var data = extractReadableContent(content);
  populateFields(1, data);
}