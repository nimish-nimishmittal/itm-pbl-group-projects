const express = require('express');
const router = express.Router();

const bcrypt = require('bcrypt');
const User = require('../models/user');

const expresssession = require('express-session');

router.get('/register',(req,res)=>{
    res.render('register');
});

router.post('/register',async (req,res)=>{
    try {
        const hashedPassword = await bcrypt.hash(req.body.password,10);
        const user = new User({
            username:req.body.username,
            password:hashedPassword
        });
        await user.save();
        res.redirect('/');
        
    } catch{
        res.redirect('/auth/register');
    }
});

router.get('/login',(req,res)=>{
    res.render('login');
});

router.post('/login',async(req,res)=>{
    const user = await User.findOne({
        username:req.body.username
    });
    if(user && await bcrypt.compare(req.body.password,user.password)){
        req.session.user = user;
        res.redirect('/');
    }
    else{
        res.redirect('/auth/login');
    }
});

module.exports = router;