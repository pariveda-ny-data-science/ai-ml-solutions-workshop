const targetJson = "samsung.json";

function avgValOfProp(arr, prop) {
  if (arr.length) {
    return arr.reduce(((sum, item) => sum + item[prop]), 0) / arr.length;
  }
}

function convertToPack(root) {
  if (!!root.length) {
    return root.map((elem, index) => {
      return {
        name: elem.title,
        url: elem.url,
        value: elem.value,
        sentiment: elem.sentiment,
        entities: elem.entities
      }
    });
  } else {
    return Object.keys(root).map(key => {
      var children = convertToPack(root[key]);
      return {
        name: key,
        children: children,
        value: root[key].length || 0,
        sentiment: avgValOfProp(children, 'sentiment'),
        entities: root[key].entities
      }
    });
  }
}

function prepData(root, outerName) {
  if (!outerName) outerName = '';

  let entityFrequency = {};
  let entityIndexMap = {};
  let entityGroupings = root.map((item, index) => {
    return {
      title: item.name,
      parent: item.category || 'Uncategorized',
      url: item.url,
      value: item.textEntities.length,
      sentiment: item.headlineSentiment,
      entities: item.textEntities.map(entity => {
        entityFrequency[entity.name] = entityFrequency[entity.name] + 1 || 1;
        entityIndexMap[entity.name] ? (entityIndexMap[entity.name].push(index)) : (entityIndexMap[entity.name] = [index]);
        return entity.name
      })
    }
  });
  let sortedFrequency = Object.entries(entityFrequency).sort((a, b) => b[1] - a[1]);

  // Starting with the most frequent entity
  let hierarchy = {};
  sortedFrequency.map((item) => {
    let entity = item[0];

    // Relate the other entities based on the groupings
    entityIndexMap[entity].map((index) => {
      let parent = entityGroupings[index].parent;
      entityGroupings[index].entities
        .filter(groupItem => groupItem !== entity && entityFrequency[groupItem])
        .map(groupItem => {
          if (!hierarchy[parent]) {
            hierarchy[parent] = {};
          }
          if (!hierarchy[parent][entity]) {
            hierarchy[parent][entity] = {};
          }
          if (!hierarchy[parent][entity][groupItem]) {
            hierarchy[parent][entity][groupItem] = [];
          }
          hierarchy[parent][entity][groupItem].push(entityGroupings[index]);

          entityFrequency[groupItem] -= 1;
        });
    });

    // Mark entity as having been "seen" 
    entityFrequency[entity] = 0;
  });

  // Get nfl data in Pack format
  let groups = convertToPack(hierarchy);
  let packaged = {
    name: outerName,
    children: groups,
    sentiment: avgValOfProp(groups, "sentiment")
  };
  return packaged;
}

d3.json(targetJson, function (error, root) {
  drawToSVG(prepData(root, targetJson));
});

var inputElement = document.getElementById("input");
inputElement.addEventListener("change", handleFiles, false);
function handleFiles() {
  var fileList = this.files; /* now you can work with the file list */
  if (fileList && fileList[0]) {
    const reader = new FileReader();
    reader.onload = function(fileLoadedEvent){
        var textFromFileLoaded = fileLoadedEvent.target.result;
        drawToSVG(prepData(JSON.parse(textFromFileLoaded), fileList[0].name));
    };
    reader.readAsText(fileList[0]);
  }
}