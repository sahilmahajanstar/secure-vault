import './style/verify.css'

import {
    VerifyEmailOTPRequestBuilder,
    VerifyEmailRequestBuilder,
} from '../../config/api/verify'
import { useAppDispatch, useAppSelector } from '../../config/redux/hooks'
import { useEffect, useMemo, useState } from 'react'

import { If } from '../../common/components/If'
import { Navigate } from 'react-router-dom'
import { userActions } from '../reducer/userReducer'
import { verifyApi } from '../../config/api'

export default function VerifyEmail() {
    const [otp, setOtp] = useState('')
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)
    const [success, setSuccess] = useState(false)
    const [resendDisabled, setResendDisabled] = useState(false)
    const [countdown, setCountdown] = useState(30)
    const [showOtpInput, setShowOtpInput] = useState(false)
    const dispatch = useAppDispatch()
    const user = useAppSelector(state => state.user.user)
    const verifyEmailRequestBuilder = useMemo(
        () => new VerifyEmailRequestBuilder(),
        [],
    )
    const verifyEmailOTPRequestBuilder = useMemo(
        () => new VerifyEmailOTPRequestBuilder(),
        [],
    )
    const sendVerificationEmail = async () => {
        try {
            if (!user?.email) {
                return
            }
            setLoading(true)
            verifyEmailRequestBuilder.setType('email_verification')
            verifyEmailRequestBuilder.setEmail(user?.email)
            await verifyApi.verifyEmail(verifyEmailRequestBuilder)
            setResendDisabled(true)
            setCountdown(60)
            setError('')
            setShowOtpInput(true)
        } catch (err: unknown) {
            const error = err as Error
            setError(error.message || 'Failed to send verification code')
        } finally {
            setLoading(false)
        }
    }

    // Handle countdown timer for resend button
    useEffect(() => {
        if (resendDisabled && countdown > 0) {
            const timer = setInterval(() => {
                setCountdown(prev => prev - 1)
            }, 1000)
            return () => clearInterval(timer)
        } else if (countdown === 0) {
            setResendDisabled(false)
        }
    }, [resendDisabled, countdown])

    useEffect(() => {
        verifyEmailOTPRequestBuilder.setOTP(otp)
    }, [otp, verifyEmailOTPRequestBuilder])
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        try {
            if (!user?.email) {
                return
            }
            setLoading(true)
            verifyEmailOTPRequestBuilder.setType('email_verification')
            verifyEmailOTPRequestBuilder.setEmail(user?.email)
            await verifyApi.validateEmailOTP(verifyEmailOTPRequestBuilder)
            dispatch(userActions.setEmailVerified(true))
            setSuccess(true)
            setError('')
        } catch (err: unknown) {
            const error = err as Error
            setError(error.message || 'An error occurred')
        } finally {
            setLoading(false)
        }
    }

    const handleResend = async () => {
        await sendVerificationEmail()
    }
    if (!user?.email) {
        return (
            <Navigate to="/users/register" state={{ from: location }} replace />
        )
    }

    return (
        <div className="verify-email-container">
            <div className="verify-email-card">
                <div className="verify-email-header">
                    <h2>Verify Your Email</h2>
                    <If condition={!showOtpInput}>
                        <p>
                            Click below to receive a verification code in your
                            email
                        </p>
                    </If>
                    <If condition={showOtpInput}>
                        <p>
                            Please enter the verification code sent to your
                            email
                        </p>
                    </If>
                </div>

                <If condition={success}>
                    <div className="success-message">
                        Email verified successfully! Redirecting...
                    </div>
                </If>

                <If condition={!success}>
                    <If condition={!showOtpInput}>
                        <div className="verify-actions">
                            <button
                                type="button"
                                className="verify-button"
                                onClick={sendVerificationEmail}
                                disabled={loading}>
                                {loading
                                    ? 'Sending...'
                                    : 'Send Verification Code'}
                            </button>
                        </div>
                    </If>

                    <If condition={showOtpInput}>
                        <form
                            onSubmit={handleSubmit}
                            className="verify-email-form">
                            <div className="form-group">
                                <label htmlFor="otp">Verification Code</label>
                                <input
                                    id="otp"
                                    type="text"
                                    value={otp}
                                    onChange={e => setOtp(e.target.value)}
                                    placeholder="Enter verification code"
                                    required
                                />
                            </div>

                            <div className="verify-actions">
                                <If condition={error}>
                                    <div className="error-message">{error}</div>
                                </If>
                                <button
                                    type="submit"
                                    className="verify-button"
                                    disabled={loading}>
                                    {loading && !showOtpInput
                                        ? 'Verifying...'
                                        : 'Verify Email'}
                                </button>

                                <button
                                    type="button"
                                    className="resend-button"
                                    onClick={handleResend}
                                    disabled={resendDisabled || loading}>
                                    {resendDisabled
                                        ? `Resend in ${countdown}s`
                                        : 'Resend Code'}
                                </button>
                            </div>
                        </form>
                    </If>
                </If>
            </div>
        </div>
    )
}
