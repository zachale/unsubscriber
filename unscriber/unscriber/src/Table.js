
export default function Table ({data}) {

    const rows = [];

    for(let i = 0; i < data.length; i++){

        rows.push(<tr>{data[i]["name"]} <button onClick={()=> window.open(data[i]["link"], "_blank")}>unsubscribe</button></tr>)

    }
 
    return(rows);
}