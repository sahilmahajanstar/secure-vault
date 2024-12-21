import { Navigate, Outlet, useLocation } from 'react-router-dom'

import React from 'react'
import VerifyEmail from '../../users/component/VerifyEmail'
import { useAppSelector } from '../../config/redux/hooks'

export const ProtectedRoute = React.memo(() => {
    const isAuthenticated = useAppSelector(state => {
        return state.user.isAuthenticated
    })
    const user = useAppSelector(state => {
        return state.user.user
    })

    const location = useLocation()

    if (!isAuthenticated) {
        return <Navigate to="/users/login" state={{ from: location }} replace />
    }
    if (!user?.emailVerified) {
        return <VerifyEmail />
    }
    return (
        <>
            <Outlet />
        </>
    )
})

export const AuthGuard = () => {
    const isAuthenticated = useAppSelector(state => {
        return state.user.isAuthenticated
    })
    const location = useLocation()

    if (isAuthenticated) {
        return (
            <Navigate
                to={location.state?.from?.pathname || '/files/list'}
                replace
            />
        )
    }
    return <Outlet />
}
