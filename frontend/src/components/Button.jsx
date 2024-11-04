import React from 'react'
import './Button.css'
export default function Button({submit,text,name}) {
  return (
   <div className='button'onClick={(e)=>{submit(e,name)}} >{text}</div>
  )
}