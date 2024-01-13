import Table from './Table';
import './App.css';
import data from './messages.json';


function App() {

  return (
    <div className="App">
      <header className="App-header">
        <Table data={data}/>
      </header>
    </div>
  );
}

 


export default App;
