import Table from './Table';
import './App.css';
import data from './messages.json';
import { GoogleLogin} from '@react-oauth/google';


function App() {

  return (
    <div className="App">

      {/* google one tap login button */}
      
      <GoogleLogin
      onSuccess={credentialResponse => {
        console.log(credentialResponse);
      }}
      onError={() => {
        console.log('Login Failed');
      }}
      useOneTap
      />;

      <header className="App-header">
        <Table data={data}/>
      </header>
    </div>
  );
}

 


export default App;
