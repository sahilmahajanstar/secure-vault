import './style/login.css'

import { Link, useNavigate } from 'react-router-dom'
import { authApi, verifyApi } from '../../config/api'
import { useEffect, useMemo, useState } from 'react'

import { If } from '../../common/components/If'
import { LoginRequestBuilder } from '../../config/api/auth'
import { VerifyEmailRequestBuilder } from '../../config/api/verify'
import { useAppDispatch } from '../../config/redux/hooks'
import { userActions } from '../reducer/userReducer'

export default function Login() {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [otp, setOtp] = useState('')
    const [showOtp, setShowOtp] = useState(false)
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate()
    const dispatch = useAppDispatch()
    const loginRequest = useMemo(() => new LoginRequestBuilder(), [])

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        try {
            if (!showOtp) {
                const request = new VerifyEmailRequestBuilder()
                request.setUsername(username)
                request.setType('login_verification')
                setLoading(true)
                await verifyApi.verifyEmail(request)
                setLoading(false)
                setShowOtp(true)
                setError('')
            } else {
                loginRequest.setOtp(otp)
                setLoading(true)
                const response = await authApi.login(loginRequest)
                setLoading(false)
                dispatch(
                    userActions.setUserInfo({
                        user: response.user!,
                        token: response.token.access,
                        refreshToken: response.token.refresh,
                    }),
                )
                navigate('/user', { replace: true })
            }
        } catch (err: unknown) {
            const error = err as Error
            setLoading(false)
            setError(error.message || 'An error occurred')
        }
    }

    const handleBack = () => {
        setShowOtp(false)
        setOtp('')
        setError('')
    }

    useEffect(() => {
        loginRequest.setUsername(username)
    }, [loginRequest, username])

    useEffect(() => {
        loginRequest.setPassword(password)
    }, [loginRequest, password])

    return (
        <div className="login-container">
            <div className="login-card">
                <div className="login-header">
                    <h2>Welcome Back</h2>
                    <p>Login to access your secure vault</p>
                </div>
                {error && <div className="error-message">{error}</div>}
                <form onSubmit={handleSubmit} className="login-form">
                    <If condition={!showOtp}>
                        <div className="form-group">
                            <label htmlFor="username">Username</label>
                            <input
                                id="username"
                                type="text"
                                value={username}
                                onChange={e => {
                                    setUsername(e.target.value)
                                }}
                                placeholder="Enter your username"
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="password">Password</label>
                            <input
                                id="password"
                                type="password"
                                value={password}
                                onChange={e => {
                                    setPassword(e.target.value)
                                }}
                                placeholder="Enter your password"
                                required
                            />
                        </div>
                    </If>
                    <If condition={showOtp}>
                        <div className="form-group">
                            <label htmlFor="otp">One-Time Password</label>
                            <input
                                id="otp"
                                type="text"
                                value={otp}
                                onChange={e => {
                                    loginRequest.setOtp(e.target.value)
                                    setOtp(e.target.value)
                                }}
                                placeholder="Enter OTP"
                                required
                            />
                            <p className="otp-hint">
                                Please enter the OTP sent to your device
                            </p>
                        </div>
                        <button
                            type="button"
                            onClick={handleBack}
                            className="back-button">
                            Back to Login
                        </button>
                    </If>
                    <button
                        type="submit"
                        className="login-button"
                        disabled={loading}>
                        {showOtp ? 'Verify OTP' : 'Continue'}
                    </button>
                </form>

                <div className="login-footer">
                    <p>
                        Don't have an account?{' '}
                        <Link to="/users/register">Create Account</Link>
                    </p>
                </div>
            </div>
        </div>
    )
}
