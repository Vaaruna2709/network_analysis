import React from 'react'
import Button from '../components/Button'
import './Home.css'
import { useNavigate } from 'react-router-dom'
export default function Home() {
  const navigate = useNavigate()
  const handleSubmit = (e,name) => {
    // console.log(e)
    if (name =='series') {
      navigate('/input-values/series')
    } else {
      navigate('/input-values/parallel')
    }
  }

  return (
    <div className='container'>
      <h3 className='app-heading'>Choose Your Circuit Type: Are you analysing a Series RLC or Parallel RLC?</h3>
      <div className="options">
        <Button submit={handleSubmit} text={'Series'} name={'series'} />
        <Button submit={handleSubmit} text={'Parallel'} name={'parallel'}/>
      </div>

    </div>
  )
}
