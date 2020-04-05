$("#search").keyup((event) => {
  updateData()
})

$("#table .fa-sort").click((event) => {
  let state = (parseInt(event.target.getAttribute("state")) + 1) % 3
  event.target.setAttribute("state", state)
  for (let j = 0; j < numColumns; j++) {
    if ($("#table thead tr .fa-sort")[j] != event.target) {
      $("#table thead tr .fa-sort")[j].setAttribute("state", 0)
    }
  }
  updateData()
})

function updateData() {
  let value = $("#search").val().toLowerCase()
  currentData = []
  for (let i = 0; i < genieData.length; i++) {
    for (let j = 0; j < numColumns; j++) {
      if (genieData[i][j].toLowerCase().includes(value)) {
        currentData.push(genieData[i])
        break
      }
    }
  }

  for (let j = 0; j < numColumns; j++) {
    let state = $("#table thead tr .fa-sort")[j].getAttribute("state")
    let factor = 0
    if (state == "1") {
      currentData.sort((a, b) => {
        if (a[j] > b[j]) {
          return -1
        } else if (a[j] < b[j]) {
          return 1
        } else {
          return 0
        }
      })
    } else if (state == "2") {
      currentData.sort((a, b) => {
        if (a[j] > b[j]) {
          return 1
        } else if (a[j] < b[j]) {
          return -1
        } else {
          return 0
        }
      })
    }
  }
  updateTable(currentData)
}

function updateTable(data) {
  let table = $("#table")
  let tbody = table.find("tbody")
  tbody.empty()
  updateQuad(data[0])
  for (let i = 0; i < data.length; i++) {
    let tr = $("<tr>")
    let row = data[i]
    for (let j = 0; j < numColumns; j++) {
      tr.append("<td>" + row[j] + "</td>")
    }
    tr.click((event) => {
      updateQuad(data[i])
    })
    tbody.append(tr)
  }

  let csv = ""
  data.forEach(function (row) {
    csv += row.join(",")
    csv += "\n"
  })
  let a = document.getElementById("export")
  a.href = "data:text/csv;charset=utf-8," + encodeURI(csv)
  a.download = "data.csv"
}

function updateQuad(data) {
  $("#histo1").empty()
  Plotly.newPlot("histo1", [{x: data[7], type: "histogram"}], {
    title: {
      text: "Gene Distribution"
    }
  })

  $("#histo2").empty()
  Plotly.newPlot("histo2", [{x: data[9], type: "histogram"}], {
    title: {
      text: "Disease Distribution"
    }
  })

  let layout = {
    margin: {
      l: 0,
      r: 0,
      b: 0,
      t: 0,
      pad: 0
    }
  }

  $("#scatter").empty()
  Plotly.newPlot("scatter", [{x: data[6], y: data[7], type: "scatter"}, {x: data[8], y: data[9], type: "scatter"}], layout)

  $("#articles1").empty()
  $.get({
    url: "/search?q=" + data[0],
    success: (data) => {
      for (let i = 0; i < data.length; i++) {
        let adiv = $("<div>")
        let atag = $("<a>" + data[i][0] + "</a>")
        atag.attr("href", data[i][1])
        adiv.append(atag)
        $("#articles1").append(adiv)
      }
    }
  })

  $("#articles2").empty()
  $.get({
    url: "/search?q=" + data[1],
    success: (data) => {
      for (let i = 0; i < data.length; i++) {
        let atag = $("<a>" + data[i][0] + "</a>")
        atag.attr("href", data[i][1])
        $("#articles2").append(atag)
      }
    }
  })
}

updateData(genieData)
