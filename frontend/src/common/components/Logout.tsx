import './styles/logout.css'

import { authApi } from '../../config/api'
import { useAppDispatch } from '../../config/redux/hooks'
import { useCallback } from 'react'
import { userActions } from '../../users/reducer/userReducer'

export default function Logout() {
    const dispatch = useAppDispatch()

    const handleLogout = useCallback(async () => {
        try {
            await authApi.logout()
            dispatch(userActions.unauthenticate())
        } catch {
            dispatch(userActions.unauthenticate())
        }
    }, [dispatch])

    return (
        <button onClick={handleLogout} className="logout-button">
            Logout
        </button>
    )
}
