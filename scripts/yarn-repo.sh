#!/bin/bash
set -euo pipefail

YARN_BASE_URL="${YARN_BASE_URL:-https://dl.yarnpkg.com/rpm}"
YARN_KEY="${YARN_KEY:-/etc/pki/rpm-gpg/RPM-GPG-KEY-YARN}"
YARN_REPO="${YARN_REPO:-/etc/yum.repos.d/yarn.repo}"

cat > "${YARN_KEY}" <<EOF
-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG v2

mQINBFf60uwBEAC43nuuPPXtJ0p11mXG0D5E1q62Kg70wX81y4qU2PaFPojOrWLA
VBn7tfmt2cQWfIXlRFGED40/Y3ttiwwew5lPNKvzdEbhMxTQwXF6FnwO/u0RYlcc
gCJvmGgWwrOat3I0RRKmQahEGYrVnlmNrfBTVXVmqx+SHdv4HgH+77lx73sNNKuE
KwbM+eTO3d2q1xd5OXFiAL+aNrO2LHqi4brsyKuj1gHyuZ8oBZgR+Gbd77X0T6Dt
a6K8WAiGn763LEX0vXQUArN7y8SgZ0GylqWUu7H87tPw6DoVIQgDqFllFJLOQXW6
LI5E/tYRydV1fIRy4PjVxD5ie6qZr4RNnoTOo+FbYD1MFzGQ/I5nfKXqRQHZ8ipV
ybFiI17TigRhl4e4NkGQ6siXutNCINjH5LHDQd5TVh9K5f86aUblGOObcwM7mTOB
dxdHVJ5tLFnLnBuAZJUF4YNwP9RILRSK/TG8E/30sg1jszzNHMoTp9GSP1pt2Z8J
jl5tpze/iDn1mnx2SUKoE/U3SWa2+/NeZb6sGF3t1VPemUrDGCbhBj9Xv47I7ISZ
J1H9/Sf5IR45v2/1/wkFn68eQmPD9o0ObPCdJREy+pG3jF4BbqXS7JvtglMdbq9a
VfSdcISRB1t3oKNiRHroxKbQebuGe8RBN9THLvt/CtdyvqBY/MLZnUnCWQARAQAB
tCBZYXJuIFJQTSBQYWNrYWdpbmcgPHlhcm5AZGFuLmN4PokCOQQTAQgAIwUCV/rS
7AIbAwcLCQgHAwIBBhUIAgkKCwQWAgMBAh4BAheAAAoJEJy7tVhpY/B/NUMP/0uk
wH9ych1s33mlq8vQEMc3nZhIzDTy51700hMOkcKYZgUeVyHbw2rVrMVWdM+WwtFZ
woQkAo2tdLRcj+VupAtNiPeiIFyjBv5qqgoLWpCoAb2nuUNQmVioOOD+4mcDVUGH
AwvGgMTcUxoJ1Z22in272AAw3WHi4Rc2Sn2dyiRsWmNSqhqfdkuYDh97Fa5Ia+0j
CO7EDWR/pykGHh7o8hQjKBUQSnfgE3EQ55e9CVGmORzxTBBR/YqiAbOHyWEXTZZi
AMZNnIai+Zng7S7YhE5RnCrgHL2c734EYB5bCJSgyjuhwr85ehG69yUCCRe8CKyk
W7UlPh+dE1J6Q+TXxpq6TFIHlCUgAtUgGaGl/0C7SDw3HO2kr5Ual85+e4JYC/tc
ATIkl3xk8RGrq6zLyX2VeawgSIYUM2DAEGOw9xTwb7Jb9qT9PDoCf7MwL46xXRuM
dgNJVH5taRpEnzCMnfpEZxyds3Cu31IGz612C72Vh6MfAVD+KTrZubRGlcIiwBQ2
uxuw4nJKecinUuTGKwUoZ2KyTUb+LDU2c3LMESNR3pC0y8H+zZcI5tCqMY9PBn3T
oOE3duUcw7pyKIl/VMov4qCVK9Xgnp81vFbTk4qAICrU+2KJXKgs929TDEpfSbdg
RFPDl4QmKzyGT3i56uOcIZJruEZp2POJssgyx7F6
=zuck
-----END PGP PUBLIC KEY BLOCK-----
EOF

cat > "${YARN_REPO}" <<EOF
[yarn]
name=Yarn Repository
baseurl=${YARN_BASE_URL}
enabled=1
gpgcheck=1
gpgkey=file://${YARN_KEY}
EOF
