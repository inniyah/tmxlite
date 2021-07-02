/*********************************************************************
Matt Marchant 2016 -2021
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

#pragma once

#include <cstddef>
#include <memory>
#include <fstream>
#include <tmxlite/Config.hpp>

namespace tmx
{

    class TMXLITE_EXPORT_API IOReader
    {
    public:
        IOReader() {};
        virtual ~IOReader() = default;
        IOReader(const IOReader&) = delete;
        IOReader& operator  = (const IOReader&) = delete;
        IOReader(IOReader&&) = default;
        IOReader& operator = (IOReader&&) = default;

        virtual void seek(std::size_t pos) = 0;
        virtual void readBytes(std::size_t count, char* buffer) = 0;
        virtual std::size_t size() = 0;
    };

    class TMXLITE_EXPORT_API IOAdapter
    {
    public:
        virtual ~IOAdapter() = default;

        virtual std::unique_ptr<IOReader> open(const std::string& name) const = 0;
    };

    class TMXLITE_EXPORT_API MemoryIOReader : public IOReader
    {
    public:
        MemoryIOReader() = delete;
        MemoryIOReader(const char* buffer, std::size_t size);
        virtual ~MemoryIOReader();

        virtual void seek(std::size_t pos);
        virtual void readBytes(std::size_t count, char* buffer);
        virtual std::size_t size();

    private:
        const char* m_buffer;
        std::size_t m_size;
    };

    class TMXLITE_EXPORT_API FilesystemIOReader : public IOReader
    {
    public:
        FilesystemIOReader() = delete;
        FilesystemIOReader(std::ifstream&& f);
        virtual ~FilesystemIOReader();

        virtual void seek(std::size_t pos);
        virtual void readBytes(std::size_t count, char* buffer);
        virtual std::size_t size();

    private:
        std::ifstream& m_stream;
        std::size_t m_size;
    };

    class TMXLITE_EXPORT_API FilesystemIOAdapter : public IOAdapter
    {
    public:
        FilesystemIOAdapter();
        virtual ~FilesystemIOAdapter() = default;

        virtual std::unique_ptr<IOReader> open(const std::string& name) const;
    };

}
