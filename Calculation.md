# The Convolution Approach


## Average field

We want the average scalar (vertical) B field experienced by the muons

\begin{equation}
\left\langle B \right\rangle = B(\textbf{x},t) \otimes M(\textbf{x},t)
\end{equation}

This invloves convolving the spacial and time structure of the muon beam and the B field. The spacial structures can be expanded into moments

\begin{equation}
B(\textbf{x},t) = \Sigma_i b_i(t)
\end{equation}

and 

\begin{equation}
M(\textbf{x},t) = \Sigma_i m_i(t)
\end{equation}


The average expierienced B field can then be expressed as the sum of products of the moments

\begin{equation}
\left\langle B \right\rangle = 
\Sigma_i b_{i}(t) \otimes m_{i}(t)
\end{equation}


wherein the convolution reduces to the weighted average

\begin{equation}
\left\langle B \right\rangle = 
 \frac{\Sigma_i \int b_{i}(t) m_{i}(t) c(t) dt}{\int c(t) dt}
\end{equation}

where $c(t)$, which is the number of muons present at time $t$, can be interpreted as the weighting factor for the average product between $b_{i}(t)$ and $m_{i}(t)$. Provided the time variable is discreetized finely enough so that, within the intervals, the spacial structure is effectivly constant, we can write

\begin{equation}
\boxed{
\left\langle B \right\rangle = 
\frac{\Sigma_{it} b_{it} m_{it} c_{t}}{\Sigma_t c_t} \equiv
\Sigma_i \left\langle B \right\rangle_i
}
\end{equation}

where, for later convience, we have defined the ith moment's contribution to $\left\langle B \right\rangle$ as $\left\langle B \right\rangle_i$ so that we can write

\begin{equation}
\boxed{
\left\langle B \right\rangle_n =
\frac{\Sigma_{t} b_{nt} m_{nt} c_{t}}{\Sigma_t c_t}
}
\end{equation}

for that of the nth moment. For further simplification, we can write $\left\langle B \right\rangle_n$ at time $\tau$ as 

\begin{equation}
\boxed{
\left\langle B \right\rangle_{n\tau} =
 b_{n\tau} m_{n\tau}
}
\end{equation}

so that 

\begin{equation}
\boxed{
\left\langle B \right\rangle_{n} = 
\frac{\Sigma_t c_t \left\langle B \right\rangle_{nt}}{\Sigma_t c_t} =
\frac{1}{C}\Sigma_t c_t \left\langle B \right\rangle_{nt}
}
\end{equation}

where we call $\Sigma_t c_t = C$.

