/*********************************************************************
Matt Marchant 2016 - 2021
http://trederia.blogspot.com

tmxlite - Zlib license.

This software is provided 'as-is', without any express or
implied warranty. In no event will the authors be held
liable for any damages arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute
it freely, subject to the following restrictions:

1. The origin of this software must not be misrepresented;
you must not claim that you wrote the original software.
If you use this software in a product, an acknowledgment
in the product documentation would be appreciated but
is not required.

2. Altered source versions must be plainly marked as such,
and must not be misrepresented as being the original software.

3. This notice may not be removed or altered from any
source distribution.
*********************************************************************/


#include <tmxlite/IO.hpp>

using namespace tmx;

FilesystemIOReader::FilesystemIOReader(std::ifstream&& stream) : m_stream(std::move(stream))
{
  m_stream.seekg(0, std::ios_base::end);
  m_size = m_stream.tellg();
  m_stream.seekg(0, std::ios_base::beg);
}

FilesystemIOReader::~FilesystemIOReader()
{

}

void FilesystemIOReader::seek(std::size_t pos)
{
    m_stream.seekg(pos);
}

void FilesystemIOReader::readBytes(char* buffer, std::size_t count)
{
    m_stream.read(buffer, count);
}

std::size_t FilesystemIOReader::size()
{
  return m_size;
}


FilesystemIOAdapter::FilesystemIOAdapter()
{
}

std::unique_ptr<IOReader> FilesystemIOAdapter::open(const std::string& name) const
{
    std::ifstream stream(name);
    if(!stream)
    {
        // TODO: better error handling?
        throw std::runtime_error("Could not open file " + name);
        return {};
    }

    return std::make_unique<FilesystemIOReader>(std::move(stream));
}
