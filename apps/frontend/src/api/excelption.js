import {logout} from '../api/auth'

const exceptionRequest = dispatch => err => {
    console.log(dispatch)
    console.log(err.response.status)
}

export default exceptionRequest
