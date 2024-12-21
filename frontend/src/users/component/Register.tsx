import { useMemo, useState } from 'react'

import { Link } from 'react-router-dom'
import { RegisterRequestBuilder } from '../../config/api/users'
import { RegisterUserValidator } from '../../config/api/validator/registerUser'
import { useAppDispatch } from '../../config/redux/hooks'
import { userActions } from '../reducer/userReducer'
import { usersApi } from '../../config/api'

export default function Register() {
    const [formData, setFormData] = useState({
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        username: '',
    })
    const [errors, setErrors] = useState<{ [key: string]: string }>({})
    const [isLoading, setIsLoading] = useState(false)
    const requestBuilder = useMemo(() => new RegisterRequestBuilder(), [])
    const dispatch = useAppDispatch()

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target
        switch (name) {
            case 'firstName':
                requestBuilder.setFirstName(value)
                break
            case 'lastName':
                requestBuilder.setLastName(value)
                break
            case 'email':
                requestBuilder.setEmail(value)
                break
            case 'password':
                requestBuilder.setPassword(value)
                break
            case 'username':
                requestBuilder.setUsername(value)
                break
        }
        setFormData(prev => ({
            ...prev,
            [name]: value,
        }))
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()

        const validation = RegisterUserValidator.validate(formData)

        if (!validation.isValid) {
            setErrors(validation.errors)
            return
        }

        try {
            setErrors({})
            setIsLoading(true)
            const response = await usersApi.register(requestBuilder)
            dispatch(
                userActions.setUserInfo({
                    user: response.user!,
                    token: response.token.access,
                    refreshToken: response.token.refresh,
                }),
            )
            setIsLoading(false)
        } catch (err) {
            setIsLoading(false)
            const error = err as Error
            console.log(error)
            setErrors({
                submit: error.message || 'Registration failed',
            })
        }
    }

    return (
        <div className="login-container">
            <div className="login-card">
                <div className="login-header">
                    <h2>Create Account</h2>
                    <p>Register to get started</p>
                </div>
                <form onSubmit={handleSubmit} className="login-form">
                    <div className="form-group">
                        <label htmlFor="firstName">First Name</label>
                        <input
                            id="firstName"
                            name="firstName"
                            type="text"
                            value={formData.firstName}
                            onChange={handleChange}
                            placeholder="Enter your first name"
                        />
                        {errors.firstName && (
                            <span className="error-message">
                                {errors.firstName}
                            </span>
                        )}
                    </div>

                    <div className="form-group">
                        <label htmlFor="lastName">Last Name</label>
                        <input
                            id="lastName"
                            name="lastName"
                            type="text"
                            value={formData.lastName}
                            onChange={handleChange}
                            placeholder="Enter your last name"
                        />
                        {errors.lastName && (
                            <span className="error-message">
                                {errors.lastName}
                            </span>
                        )}
                    </div>

                    <div className="form-group">
                        <label htmlFor="email">Email</label>
                        <input
                            id="email"
                            name="email"
                            type="email"
                            value={formData.email}
                            onChange={handleChange}
                            placeholder="Enter your email"
                        />
                        {errors.email && (
                            <span className="error-message">
                                {errors.email}
                            </span>
                        )}
                    </div>

                    <div className="form-group">
                        <label htmlFor="username">Username</label>
                        <input
                            id="username"
                            name="username"
                            type="text"
                            value={formData.username}
                            onChange={handleChange}
                            placeholder="Enter your username"
                        />
                        {errors.username && (
                            <span className="error-message">
                                {errors.username}
                            </span>
                        )}
                    </div>

                    <div className="form-group">
                        <label htmlFor="password">Password</label>
                        <input
                            id="password"
                            name="password"
                            type="password"
                            value={formData.password}
                            onChange={handleChange}
                            placeholder="Enter your password"
                        />
                        {errors.password && (
                            <span className="error-message">
                                {errors.password}
                            </span>
                        )}
                    </div>
                    {errors.submit && (
                        <div className="error-message">{errors.submit}</div>
                    )}

                    <button
                        type="submit"
                        className="login-button"
                        disabled={isLoading}>
                        Register
                    </button>
                </form>

                <div className="login-footer">
                    <p>
                        Already have an account?{' '}
                        <Link to="/users/login">Login</Link>
                    </p>
                </div>
            </div>
        </div>
    )
}
