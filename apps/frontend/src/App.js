import React, { useState } from 'react'


import Login from './pages/Login'


function App() {
  const [isAuth, setIsAuth] = useState(false)

  const authorization = () => {
    setIsAuth(!isAuth)
  }

  return (
    <div>
      {!isAuth ? <Login auth={authorization}/>
      
      : <div>
          Qwerty12345
        </div>}
    </div>
  );
}

export default App;
